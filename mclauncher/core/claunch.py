
"""
EDIT ON 07/30/23
claunch.py: To add a new launching way with /mclauncher/plugins/cmcl.jar
"""

import os
import subprocess
import portablemc

from .command import *
from .utils import *

cwd=os.getcwd()

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

def login_littleskin():
    os.system('start java -jar '+cwd+'/mclauncher/plugins/cmcl.jar account --login=authlib --address=https://littleskin.cn/api/yggdrasil')

def mend(vername=LATEST_MINECRAFT_STABLE):
    print('[INFO]completing assets...')
    subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --complete assets')
    print('\n[INFO]completing libraries...')
    subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --complete libraries')
    print('\n[INFO]completing natives...')
    subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --complete natives')
    print('[INFO]done completing files.')

def claunch(vername=LATEST_MINECRAFT_STABLE,force_mend=False):
        print(vername)
        vername=str(vername)
        f=open(cwd+'/mclauncher/plugins/cmcl.json','r')
        f.close()
        subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar --list='+cwd+'/.minecraft')
        subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar config checkAccountBeforeStart false')
        if force_mend == True:
            print('[INFO]completing assets...')
            subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --complete assets')
            print('\n[INFO]completing libraries...')
            subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --complete libraries')
            print('\n[INFO]completing natives...')
            subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --complete natives')
            print('[INFO]done completing files.')
        subprocess.run('del /q "'+cwd+'/latestlaunch.ps1"')
        subprocess.run('rm "'+cwd+'/latestlaunch.sh"')
        subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --export-script-ps='+cwd+'/latestlaunch.ps1')
        subprocess.run('java -jar '+cwd+'/mclauncher/plugins/cmcl.jar version "'+vername+'" --export-script='+cwd+'/latestlaunch.sh')
        print('[INFO]launching Script Generated!')
        if os.name == 'nt':
            subprocess.run('powershell Set-ExecutionPolicy -Scope CurrentUser ByPass')
            print('[INFO]powershell script unlocked!')
        if os.name == 'nt':
            c=('powershell "'+cwd+'/latestlaunch.ps1"')
        else:
            c=('bash "'+cwd+'/latestlaunch.sh"')
        p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p
