import os
import shutil
import ctypes

current_dir = os.path.dirname(os.path.abspath(__file__))
exclude_files = {'hook_manager.py', 'install.py'}
exclude_dirs = {'plugins'}

for item in os.listdir(current_dir):
    item_path = os.path.join(current_dir, item)
    
    if item in exclude_files:
        continue

    if os.path.isdir(item_path) and item in exclude_dirs:
        continue

    if os.path.isfile(item_path):
        os.remove(item_path)
        print(f"Deleted file: {item_path}")
        
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)
        print(f"Deleted directory: {item_path}")

ctypes.windll.user32.MessageBoxW(0, "You can now delete the install.py file as you won't need it anymore.", "Cleanup Complete", 0x40 | 0x1)