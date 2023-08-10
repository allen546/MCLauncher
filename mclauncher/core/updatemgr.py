
#EDIT ON 08/10/2023

#forked form ccjjfdyqlhy/PyClone

import os
import shutil
import requests
from git import Repo

def download_repo(repo_url, output_dir):
    # Clone the repository
    repo = Repo.clone_from(repo_url, output_dir)

    # Download additional files
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            download_file(file_path)

def download_file(file_path):
    # Download the file
    url = 'https://raw.githubusercontent.com' + file_path.split('github.com')[1]
    response = requests.get(url, stream=True)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the file
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)

    # Close the response
    response.close()


def updateALL(repo_url,output_dir):
    try:
        download_repo(repo_url, output_dir)
    except IndexError:
        print('[updatemgr] Operation Success.')