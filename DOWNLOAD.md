# ProgramHooks - Download & Implement

Welcome to the **ProgramHooks** framework! This document will guide you through downloading the framework, understanding its open-source nature, and implementing it into your projects and applications.

## Downloading the Framework

To download the main framework files, you have two options:

### Option 1: Clone the Repository

You can clone the repository using Git, which will allow you to get the latest updates easily.

1. Open your terminal or command prompt.
2. Run the following command:

   ```bash
   git clone https://github.com/yourusername/ProgramHooks.git
   ```

### Option 2: Download as ZIP

If you prefer, you can download the repository as a ZIP file.

1. Go to the [ProgramHooks GitHub page](https://github.com/yourusername/ProgramHooks).
2. Click on the green "Code" button.
3. Select "Download ZIP".
4. Extract the contents to your desired location.

### After Downloading the Repository

Once you have downloaded the repository, you can delete the following files as they aren't needed for the script to function:
- .gitignore
- example.py
- LICENSE
- README.md
- v1example.png
- plugins/Example.py (DO NOT REMOVE THE PLUGINS FOLDER)

You should be left with:
- /plugins (The plugins folder which contains _internal.py)
- hook_manager.py

This will help keep your project directory clean and focused on the necessary files.

### Main Framework File

The main framework file is `hook_manager.py`. This file contains the core logic for managing hooks and loading plugins.

## Open Source

**ProgramHooks** is open-source, meaning you have the freedom to modify, distribute, and use it in your own projects. This encourages collaboration and innovation within the community.

### Modifying the Framework

If you want to customize the framework, simply edit the `hook_manager.py` file or any other component as per your requirements. Please note that while you are free to modify the framework, it is encouraged to leave the original credits intact for proper acknowledgment.

### Removing Credits

If you choose to remove the credits from the code, please consider acknowledging the work in another way, such as in your project's documentation or website by linking [the github repository](https://github.com/ftnick/ProgramHooks). The credits are located in comments within the `_internal.py` file in the plugins folder and can be easily removed.

## Implementing ProgramHooks into Your Projects

To implement **ProgramHooks** in your projects, follow these steps:

1. **Include the Framework**: Copy the `hook_manager.py` file and the `plugins` directory into your project directory.

2. **Create Your Plugins**: In the `plugins` directory, create Python scripts defining your hooks. Each script should contain functions for the hook stages you wish to utilize (e.g., `pre_init`, `post_init`, `pre_runtime`, `post_runtime`).

3. **Customize Hooks**: You can pass arguments to hooks for additional functionality. For example, modify the function signatures in your plugins to accept parameters.

### Example Plugin Structure

```python
# plugins/my_plugin.py
def pre_init(init_data, **kwargs):
    print(f"Pre-Init: {init_data}, Additional Config: {kwargs}")

def post_runtime(user_id=None):
    print(f"Post-Runtime User ID: {user_id}")
```

## End

For any questions or further assistance, feel free to open an issue on the repository.

Happy coding!