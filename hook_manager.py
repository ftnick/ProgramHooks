import importlib
import os
import glob
import inspect
import sys
import time
import structlog

# Central Hook Manager
# Last Updated: 5/10/2024
# @ftnick

structlog.stdlib.recreate_defaults()
logger = structlog.get_logger("HookManager")

class HookManager:
    def __init__(self):
        self.hooks = {
            'internal': [],
            'pre_init': [],
            'post_init': [],
            'pre_runtime': [],
            'post_runtime': [],
        }

    def register_hook(self, stage, func):
        """ Register a function to a specific hook stage """
        if stage in self.hooks:
            self.hooks[stage].append(func)
        else:
            logger.error("Invalid hook stage passed to register_hook", stage=stage)
    
    def execute_hooks(self, stage, *args, **kwargs):
        """ Execute all hooks registered for a specific stage with optional arguments """
        if stage in self.hooks:
            if not self.hooks[stage]:
                logger.warning(f"No hooks found for stage: {stage}, but still executed void")
            for hook in self.hooks[stage]:
                logger.info(f"Executing {hook.__name__}", alternate=stage)
                try:
                    hook(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Failed to execute {hook.__name__}", error=e)
        else:
            logger.critical(
                f"Unexpected Program Error: Invalid stage provided: '{stage}'",
                note="If you encounter this error, it is likely due to an unexpected coding issue or a malfunctioning feature. Please report this to us as soon as possible for further investigation."
            )

    def load_plugins(self, plugin_folder):
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
            except Exception:
                logger.warning("Failed to load plugin ", plugin=module_name)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Loaded {valid_plugins} Plugin(s)", duration=f"{duration:.6f} seconds")

    def _register_module_hooks(self, module):
        """ Register functions from a module if they match hook names """
        start_time = time.time()
        valid_hooks = 0
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name in self.hooks:
                logger.info(f"Registering {name} from {module.__name__}")
                try:
                    self.register_hook(name, func)
                    valid_hooks += 1
                except Exception:
                    logger.error("Failed to register plugin hook ", plugin=module.__name__, hook=name, hook_func=func)
            else:
                logger.warning(f"The '{name}' function inside the valid plugin file '{module.__name__}' is not an actual stage, consider removing the function from the plugin")
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Loaded {valid_hooks} Hook(s) from {module.__name__}", duration=f"{duration:.6f} seconds")