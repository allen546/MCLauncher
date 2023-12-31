import os
import os.path
import pathlib
import platform

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
    
