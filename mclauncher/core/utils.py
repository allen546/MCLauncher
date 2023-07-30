import os
import os.path
import pathlib
import platform
from functools import partial

cwd=os.getcwd()

VERSIONS_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"

def init_minecraft_directory() -> str:
    """
    Return and set the default path to the .minecraft directory
    """
    try:
        open(cwd+'/config/mc_inst_dir.cfg')
    except FileNotFoundError:
        if platform.system() == "Windows":
            os.system('mkdir config')
            with open(cwd+'/config/mc_inst_dir.cfg','w') as f:
                f.write(os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".minecraft"))
                print('done')
            return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".minecraft")
        elif platform.system() == "Darwin":
            os.system('mkdir config')
            with open(cwd+'/config/mc_inst_dir.cfg','w') as f:
                f.write(os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft"))            
            return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft")
        else:
            os.system('mkdir config')
            with open(cwd+'/config/mc_inst_dir.cfg','w') as f:
                f.write(os.path.join(str(pathlib.Path.home()), ".minecraft"))
            return os.path.join(str(pathlib.Path.home()), ".minecraft")
        
def edit_minecraft_directory(dest):
    """
    Edit the minecraft_directory path
    """
    try:
        f=open(cwd+'/config/mc_inst_dir.cfg','w')
        f.write(dest)
        print('done')
    except FileNotFoundError:
        print('Original file not found')
    
class ButtonGroup():
    def __init__(self):
        self.buttons = []

    def set_onclick(self, function, args=None, kwargs=None):
        if not args: args = []
        if not kwargs: kwargs = {}
        func = partial(function, *args, **kwargs)
        for btn in self.buttons:
            btn.on("click", func)

    def add_button(self, btn):
        self.buttons.append(btn)

    def disable(self):
        for btn in self.buttons:
            btn.disable()

    def enable(self):
        for btn in self.buttons:
            btn.enable()