import os.path
from .installjdk import install

def install_all_used_java(path="~/.jdk/"):
    path = os.path.expanduser(path)
    #install("8u351", jre=True, path=os.path.join(path, "8u351"), impl="adoptium")
    install("11", jre=True, path=os.path.join(path, "11"), impl="adoptium")
    install("17", jre=True, path=os.path.join(path, "17"), impl="adoptium")