# ProgramHooks - Download & Implement

Welcome to the **ProgramHooks** framework! This document will guide you through downloading the framework, understanding its open-source nature, and implementing it into your projects and applications.

---

### Downloading the ProgramHooks Framework

You have two options for downloading the framework, depending on your needs:

#### 1. Full Example Package (Recommended for Learning)
This package is ideal if you want to explore how the framework works with examples. It includes:

- **`example.py`**: A sample script demonstrating how to use the framework via `hook_manager.py`.  
  ![Example Script Output](https://raw.githubusercontent.com/ftnick/ProgramHooks/refs/heads/main/v1example.png)
  
- **`hook_manager.py`**: The core framework file, which can be imported into other Python scripts to create custom hook-based functionalities.
  
- **`plugins/` folder**: A collection of pre-installed plugins that serve as working examples for expanding functionality through hooks.

**Download the Full Example Package**:  
[Click here](https://programhooks.ftnick.xyz/download?package=full) to download the complete package, including the example script and plugins.

#### 2. Main Framework File Only (For Experienced Users)
If you're familiar with Python frameworks and just want the core file without the extras, you can download only the main framework file.

- **`hook_manager.py`**: The core framework file that you can integrate directly into your projects.

**Download the Main Framework File**:  
[Click here](https://programhooks.ftnick.xyz/download?package=frameworkonly) to download just the framework file.

---

### Main Framework File

The main framework file is `hook_manager.py`. This file contains the core logic for managing hooks and loading plugins.

---

## Open Source

**ProgramHooks** is open-source, meaning you have the freedom to modify, distribute, and use it in your own projects. This encourages collaboration and innovation within the community.

---

### Modifying the Framework

If you want to customize the framework, simply edit the `hook_manager.py` file or any other component as per your requirements. Please note that while you are free to modify the framework, it is encouraged to leave the original credits intact for proper acknowledgment.

---

### Removing Credits

If you choose to remove the credits from the code, please consider acknowledging the work in another way, such as in your project's documentation or website by linking [the github repository](https://github.com/ftnick/ProgramHooks). The credits are located in comments within the `_internal.py` file in the plugins folder and can be easily removed.

---

### Implementing ProgramHooks into Your Projects

To implement **ProgramHooks** in your projects, follow these steps:

1. **Include the Framework**: Copy the `hook_manager.py` file and create a `plugins` directory into your project directory.

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
