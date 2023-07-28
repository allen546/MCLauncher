import os.path
from jdk import install

def install_all_used_java(path="~/.jdk/"):
    path = os.path.expanduser(path)
    install("8u351", jre=True, path=os.path.join(path, "8u351"))
    install("11", jre=True, path=os.path.join(path, "11"))
    install("17", jre=True, path=os.path.join(path, "17"))