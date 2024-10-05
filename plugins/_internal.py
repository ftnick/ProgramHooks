import os

def pre_init():
    os.makedirs("plugins", exist_ok=True)

def pre_runtime():
    print("This application uses ProgramHooks by @ftnick")