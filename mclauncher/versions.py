import requests

VERSIONS_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"

class MinecraftVersion():
    @classmethod
    def get_all(cls):
        versions = requests.get(VERSIONS_URL)
        versions.raise_for_status()
        return(versions.json) # Not finished, return json for now, return a MinecraftVersion list/dict later