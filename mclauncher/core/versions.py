import json

class VersionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Version):
            return {"__type__":"MinecraftVersion", "version":str(obj.name),"type":obj.type}

        return super().default(self, obj)
    
def VersionDecoder(dct):
    if "__type__" in dct and dct["__type__"] == "MinecraftVersion":
        return Version(version_name=dct["version"], version_type=dct["type"])
    return dct

def VersionDecoder2(dct):
    if isinstance(VersionDecoder(dct), Version):
        return VersionDecoder(dct).type.capitalize() + " " + VersionDecoder(dct).name
    return dct

class Version:
    def load_from(filename):
        """
        Load a version list from a JSON file.
        """
        with open(filename, "r") as f:
            j = json.load(f, object_hook=VersionDecoder)

        return j

    def __init__(self, version_name, version_type):
        self.name = version_name
        self.type = version_type

    def __repr__(self):
        return self.name
    

