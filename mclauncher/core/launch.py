import portablemc
import subprocess
from .command import *
from .utils import *

LATEST_MINECRAFT_STABLE = portablemc.VersionManifest().filter_latest("release")[0]

def quickstart(minecraft_version=LATEST_MINECRAFT_STABLE, username="steve"):
    command = Command("portablemc", ["start", str(minecraft_version)], {"-u": username})
    c = command.build()
    p = subprocess.Popen(c)
    return p
