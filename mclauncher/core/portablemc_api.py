import os
from portablemc import *
from .jvm import *

CACHED_VERSION_MANIFEST = os.path.join(get_minecraft_dir(), "version_manifest.json")

class Minecraft:
    def __init__(self, version, main_dir=get_minecraft_dir()):
        self.ctx = Context(main_dir, main_dir)
        self.version_manifest = VersionManifest(CACHED_VERSION_MANIFEST, 64)
        try:
            self.version = Version(self.version_manifest.get_version(version))
        except VersionError: raise

        
    def prepare_mc(self):
        try:
            self.version.install(jvm=False)
        except Exception as e:
            return e
