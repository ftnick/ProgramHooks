import importlib
import os
import glob
import inspect
import sys
import time
import structlog
import requests
import threading
from typing import Callable, Dict, List, Any
from packaging.version import Version, InvalidVersion

# Central Hook Manager
# Last Updated: 5/10/2024
# @ftnick
CURRENT_VERSION = "v1.3"

os.makedirs("plugins", exist_ok=True)

structlog.stdlib.recreate_defaults()
logger = structlog.get_logger("HookManager")

def is_prerelease(version_str: str) -> bool:
    """Determine if the version string corresponds to a pre-release."""
    try:
        version = Version(version_str)
        return version.is_prerelease
    except InvalidVersion:
        return False

def get_numeric_version(version_str: str) -> str:
    """Extract the numeric part of the version string."""
    try:
        return Version(version_str).base_version
    except InvalidVersion:
        return None

try:
    response = requests.get("https://api.github.com/repos/ftnick/ProgramHooks/releases")
    response.raise_for_status()
    releases = response.json()
    latest_version = Version(CURRENT_VERSION)
    latest_release_tag = None
    if releases:
        for release in releases:
            release_tag = release["tag_name"].lstrip("v")
            try:
                release_version = Version(release_tag)
            except InvalidVersion:
                logger.debug(f"Skipping invalid version tag: {release_tag}")
                continue
            if release["prerelease"] or release_version.is_prerelease:
                logger.debug(f"Skipping prerelease version: {release_tag}")
                continue
            if release_version > latest_version:
                latest_version = release_version
                latest_release_tag = release_tag
        if latest_version == Version(CURRENT_VERSION):
            logger.info(f"Your script is up-to-date with version {CURRENT_VERSION}.")
        elif latest_version > Version(CURRENT_VERSION):
            logger.warning(
                f"Your script is outdated! Latest release is version {latest_release_tag}, "
                f"but you're using version {CURRENT_VERSION}."
            )
    else:
        logger.info("No releases found for the repository.")
except requests.exceptions.RequestException as e:
    logger.error("Failed to check for ProgramHook updates", error=str(e))
    
def rwt(func, args=(), kwargs=None, timeout=10, hook_name="Function"):
    if kwargs is None:
        kwargs = {}
    result = [None]
    def target():
        result[0] = func(*args, **kwargs)
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        logger.warning(f"A hook function for {hook_name} has exceeded the set timeout parameter. The thread has been terminated.")
        return None
    else:
        return result[0]

class HookManager:
    def __init__(self, stages: List[str] = None):
        """
        Initialize the HookManager with default stages.

        Args:
            stages: List of hook stages to initialize. If None, defaults to
            ['pre_init', 'post_init', 'pre_runtime', 'post_runtime'].
        """
        if stages is None:
            stages = ["pre_init", "post_init", "pre_runtime", "post_runtime"]
        self.hooks: Dict[str, List[Callable]] = {stage: [] for stage in stages}

    def register_hook(self, stage: str, func: Callable) -> None:
        """Register a function to a specific hook stage.

        Args:
            stage: The stage to register the hook to.
            func: The function to be registered.
        """
        if stage in self.hooks:
            self.hooks[stage].append(func)
            logger.info(f"Registered hook '{func.__name__}' at stage '{stage}'")
        else:
            logger.error("Invalid hook stage passed to register_hook", stage=stage)

    def execute_hooks(self, stage: str, *args: Any, **kwargs: Any) -> None:
        """Execute all hooks registered for a specific stage with optional arguments.

        Args:
            stage: The stage to execute hooks for.
            args: Positional arguments to pass to hooks.
            kwargs: Keyword arguments to pass to hooks.
        """
        if stage not in self.hooks:
            logger.critical(
                f"Unexpected Program Error: Invalid stage provided: '{stage}'",
                note="If you encounter this error, it is likely due to an unexpected coding issue or a malfunctioning feature. Please report this to us as soon as possible for further investigation.",
            )
            return

        if not self.hooks[stage]:
            logger.warning(
                f"No hooks found for stage: {stage}, but still executed void"
            )

        for hook in self.hooks[stage]:
            logger.info(f"Executing {hook.__name__} for stage: {stage}")
            try:
                rwt(hook, *args, **kwargs, hook_name = hook.__name__)
                # hook(*args, **kwargs) #* No timeout method
            except Exception as e:
                logger.error(f"Failed to execute {hook.__name__}", error=str(e))

    def load_plugins(self, plugin_folder: str) -> None:
        """Load plugins from a specified folder.

        Args:
            plugin_folder: The folder containing plugin files.
        """
        logger.info("Loading Plugins...")
        start_time = time.time()
        sys.path.append(os.path.abspath(plugin_folder))
        valid_plugins = 0
        py_files = glob.glob(os.path.join(plugin_folder, "*.py"))

        for py_file in py_files:
            module_name = os.path.splitext(os.path.basename(py_file))[0]
            try:
                module = importlib.import_module(module_name)
                self._register_module_hooks(module)
                valid_plugins += 1
                logger.debug("Loaded plugin", plugin=module_name)
            except ImportError as e:
                logger.warning(
                    "Failed to load plugin", plugin=module_name, error=str(e)
                )
            except Exception as e:
                logger.warning(
                    "An unexpected error occurred while loading plugin",
                    plugin=module_name,
                    error=str(e),
                )

        end_time = time.time()
        duration = end_time - start_time
        logger.info(
            f"Loaded {valid_plugins} Plugin(s)", duration=f"{duration:.6f} seconds"
        )

    def _register_module_hooks(self, module: Any) -> None:
        """Register functions from a module if they match hook names.

        Args:
            module: The module to register hooks from.
        """
        start_time = time.time()
        valid_hooks = 0

        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name in self.hooks:
                logger.info(f"Registering {name} from {module.__name__}")
                try:
                    self.register_hook(name, func)
                    valid_hooks += 1
                except Exception as e:
                    logger.error(
                        "Failed to register plugin hook",
                        plugin=module.__name__,
                        hook=name,
                        hook_func=func,
                        error=str(e),
                    )
            else:
                logger.warning(
                    f"The '{name}' function inside the valid plugin file '{module.__name__}' is not an actual stage, consider removing the function from the plugin"
                )

        end_time = time.time()
        duration = end_time - start_time
        logger.info(
            f"Loaded {valid_hooks} Hook(s) from {module.__name__}",
            duration=f"{duration:.6f} seconds",
        )


if __name__ == "__main__":
    message = (
        "Warning: This script is not intended to be run directly. "
        "It should be imported along with its class, HookManager. "
        "For usage details, please visit: https://github.com/ftnick/ProgramHooks"
    )
    logger.fatal(message)
    input("Press Enter to exit...")
