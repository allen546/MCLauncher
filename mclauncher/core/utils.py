import os
import os.path
import pathlib
import platform
from functools import partial

VERSIONS_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"

def get_minecraft_directory() -> str:
    """
    Returns the default path to the .minecraft directory
    """
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".minecraft")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft")
    else:
        return os.path.join(str(pathlib.Path.home()), ".minecraft")
    
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