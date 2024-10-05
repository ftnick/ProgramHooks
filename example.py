# Import the HookManager class from the hook_manager module
from hook_manager import HookManager

# Import structlog for structured logging
import structlog

# Recreate default settings for structured logging
structlog.stdlib.recreate_defaults()

# Create a logger instance for the main application
logger = structlog.get_logger("Main")

# Initialize an instance of the HookManager
hook_manager = HookManager()

# Load all plugins from the 'plugins' directory
# This scans the specified folder and registers any hooks defined in the plugins
hook_manager.load_plugins('plugins')

# Execute the pre-initialization hooks
# This will call all registered functions for the 'pre_init' stage
hook_manager.execute_hooks('pre_init')

# Execute the post-initialization hooks
# This will call all registered functions for the 'post_init' stage
hook_manager.execute_hooks('post_init')

# Execute the pre-runtime hooks
# This will call all registered functions for the 'pre_runtime' stage
hook_manager.execute_hooks('pre_runtime')

# Indicate that the main runtime of the application is starting
print("start runtime..")

# Simulate the main logic of your application here
# You can add your main functionality or core loops

# Indicate that the runtime of the application is stopping
print("stop runtime..")

# Execute the post-runtime hooks
# This will call all registered functions for the 'post_runtime' stage
hook_manager.execute_hooks('post_runtime')

# Pause the program
# This will keep the console open until the user presses Enter
input("DEBUG PAUSE (IGNORE, END OF SCRIPT)")
