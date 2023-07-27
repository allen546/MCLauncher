import portablemc
import subprocess
from .command import *
from .utils import *
import os

LATEST_MINECRAFT_STABLE = portablemc.VersionManifest().filter_latest("release")[0]
if os.name != "nt":
    _jvm = subprocess.check_output(["which", "java"]).decode("utf-8").strip()
    JVM_SHOULD_BE = _jvm
else: 
    JVM_SHOULD_BE = None

def quickstart(minecraft_version=LATEST_MINECRAFT_STABLE, username="steve", JVM=JVM_SHOULD_BE):
    if JVM:
        command = Command("portablemc", ["start", str(minecraft_version), "--jvm="+JVM], {"-u": username})
    else:
        command = Command("portablemc", ["start", str(minecraft_version)], {"-u": username})
    c = command.build()
    p = subprocess.Popen(c)
    return p
