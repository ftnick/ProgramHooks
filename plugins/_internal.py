import os

def pre_init():
    os.makedirs("plugins", exist_ok=True) #? if theres no plugins folder why is this plugin being loaded????? #2amcoding

def pre_runtime():
    print("This application uses ProgramHooks by @ftnick")