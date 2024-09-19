import os
import shutil
import subprocess

# Function to delete files from specified folders
def delete_files(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Deletes the folder and its contents
        os.makedirs(folder_path)  # Recreate an empty folder
        print(f"Deleted and recreated folder: {folder_path}")
    else:
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")

# Delete files from 'temp' and 'cleaned' folders
delete_files('./temp')
delete_files('./cleaned')

# Now call the scripts in sequence
try:
    subprocess.run(['python3', './scripts/fs_cleanup.py'], check=True)
    subprocess.run(['python3', './scripts/ebu_cleanup.py'], check=True)
    subprocess.run(['python3', './scripts/bd_cleanup.py'], check=True)
    print("All scripts ran successfully.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running a script: {e}")