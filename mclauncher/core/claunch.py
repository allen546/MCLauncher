
"""
EDIT ON 07/30/23
claunch.py: To add a new launching way with /plugins/cmcl.jar
"""

import os
import subprocess

cwd=os.getcwd()

def login_littleskin():
    subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar account --login=authlib --address=https://littleskin.cn/api/yggdrasil')

def mend(vername):
    print('[INFO]completing assets...')
    subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --complete assets')
    print('\n[INFO]completing libraries...')
    subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --complete libraries')
    print('\n[INFO]completing natives...')
    subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --complete natives')
    print('[INFO]done completing files.')

def claunch(vername,force_mend):
    try:
        f=open(cwd+'/plugins/cmcl.json','r')
        f.close()
        subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar --list='+cwd+'/.minecraft')
        subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar config checkAccountBeforeStart false')
        if force_mend == 1:
            print('[INFO]completing assets...')
            subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --complete assets')
            print('\n[INFO]completing libraries...')
            subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --complete libraries')
            print('\n[INFO]completing natives...')
            subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --complete natives')
            print('[INFO]done completing files.')
        subprocess.run('del /q "'+cwd+'\latestlaunch.ps1"')
        subprocess.run('rm "'+cwd+'\latestlaunch.sh"')
        subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --export-script-ps='+cwd+'/latestlaunch.ps1')
        subprocess.run('java -jar '+cwd+'/plugins/cmcl.jar version "'+vername+'" --export-script='+cwd+'/latestlaunch.sh')
        print('[INFO]launching Script Generated!')
        subprocess.run('powershell Set-ExecutionPolicy -Scope CurrentUser ByPass')
        print('[INFO]powershell script unlocked!')
        subprocess.run('powershell "'+cwd+'/latestlaunch.ps1"')
        subprocess.run('bash "'+cwd+'/latestlaunch.sh"')
        print('[INFO]progress started.')
    except FileNotFoundError:
        return 2
