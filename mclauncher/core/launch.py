import tempfile
import portablemc
import subprocess
from .command import *
from .utils import *
import os

LATEST_MINECRAFT_STABLE = portablemc.VersionManifest().filter_latest("release")[0]
if os.name != "nt":
    _jvm = subprocess.check_output(["which", "java"]).decode("utf-8").strip()
    if _jvm.endswith("not found"):
        JVM_SHOULD_BE = None
    else:
        JVM_SHOULD_BE = _jvm
else: 
    _jvm = subprocess.check_output(["where", "java"]).decode("utf-8").strip()
    if "\\" in _jvm:
        JVM_SHOULD_BE = _jvm
    else:
        JVM_SHOULD_BE = None

def quickstart(minecraft_version=LATEST_MINECRAFT_STABLE, JVM=JVM_SHOULD_BE,username='steve',mslogin='',msarg=''):
    if JVM:
        if msarg == '-m':
            command = Command("portablemc", ["start", str(minecraft_version), "--jvm="+JVM], {"-u": username, msarg+" -l": mslogin})
        else:
            command = Command("portablemc", ["start", str(minecraft_version), "--jvm="+JVM], {"-u": username})
    else:
        if msarg == '-m':
            command = Command("portablemc", ["start", str(minecraft_version)], {"-u": username, msarg+" -l": mslogin})
        else:
            command = Command("portablemc", ["start", str(minecraft_version)], {"-u": username})
    c = command.build()
    print(c)
    p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p
