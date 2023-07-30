import os
import subprocess
from portablemc import *
from .jvm import *

CACHED_VERSION_MANIFEST = os.path.join(get_minecraft_dir(), "version_manifest.json")
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


class Minecraft:
    def __init__(self, version, main_dir=get_minecraft_dir()):
        self.ctx = Context(main_dir, main_dir)
        self.version_manifest = VersionManifest(CACHED_VERSION_MANIFEST, 64)
        try:
            self.version = Version(self.ctx, self.version_manifest.get_version(version)["id"])
        except VersionError: raise
        self.start_opts = StartOptions()
        self.start_opts.jvm_exec = JVM_SHOULD_BE
        #self.finalize()
        
    def prepare_mc(self):
        try:
            self.version.install(jvm=False)
        except Exception as e:
            return e
        
    def finalize(self):
        self.start = Start(self.version)
        self.start.prepare(self.start_opts)
        
    def prepare_java(self):
        pass

    def launch(self):
        self.start.start()
