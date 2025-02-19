import argparse
import shutil
import os

from downloadMod import download_CurseForgeMOD, download_ModrinthMOD
from file import unZIP, loadJsonFile

def CurseForgeOperation(file_path, folder_name):
    unZIP(file_path, folder_name)
    json_file_path = f'{folder_name}/manifest.json'
    manifestData = loadJsonFile(json_file_path)
    downloaded = 0; total_files = 0

    if "files" in manifestData:
        total_files = len(manifestData["files"])
        for index, file_entry in enumerate(manifestData["files"], start=1):
            project_id = int(file_entry.get("projectID", 0))
            file_id = int(file_entry.get("fileID", 0))

            success = download_CurseForgeMOD(project_id, file_id, index, total_files, f"{folder_name}/overrides/mods")
            if success: downloaded = downloaded + 1
    else:
        print("Missing 'files' section in JSON.")
    
    print(f'Downloaded [{downloaded}/{total_files}] mods')

def ModrinthOperation(file_path, folder_name):
    zip_path = file_path.rsplit('.', 1)[0] + ".zip"
    shutil.copy2(file_path, zip_path)
    unZIP(zip_path, folder_name)
    json_file_path = f'{folder_name}/modrinth.index.json'
    manifestData = loadJsonFile(json_file_path)
    downloaded = 0; total_files = 0
    if "files" in manifestData:
        total_files = len(manifestData["files"])
        for index, file_entry in enumerate(manifestData["files"], start=1):
            path = file_entry.get("path", "")
            downloads = file_entry.get("downloads", [])

            if downloads:
                download_url = downloads[0]
                if not os.path.isabs(path):
                    success = download_ModrinthMOD(download_url, path, index, total_files, f"{folder_name}/overrides")
                    if success: downloaded = downloaded + 1
    else:
        print("Missing 'files' section in JSON.")
    
    print(f'Downloaded [{downloaded}/{total_files}] mods')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MinecraftModPackDownloader", description="Download mods for modpack")
    parser.add_argument("file", help="Path to .zip / .mrpack file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--curseforge", action="store_true", help="Flag for downloading mods from CurseForge")
    group.add_argument("--modrinth", action="store_true", help="Flag for downloading mods from Modrinth")

    args = parser.parse_args()
    file_path = args.file
    folder_name = os.path.splitext(os.path.basename(file_path))[0]

    if args.curseforge:
        CurseForgeOperation(file_path, folder_name)
    elif args.modrinth:
        ModrinthOperation(file_path, folder_name)
    else:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.zip':
            CurseForgeOperation(file_path, folder_name)
        elif file_extension == '.mrpack':
            ModrinthOperation(file_path, folder_name)


    