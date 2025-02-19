import urllib.request
import json
import zipfile
import argparse
import shutil
import time
import os
from progressBar import progress_bar_downloading, progress_bar_unzipping

URL_CURSEFORGE_INFO = "https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}"
URL_CURSEFORGE_DOWNLOAD = "https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}/download"

def download_CurseForgeMOD(project_id, file_id, fileNumber, totalNumber, folder="mods"):
    url_info = URL_CURSEFORGE_INFO.format(project_id=project_id, file_id=file_id)
    url_download = URL_CURSEFORGE_DOWNLOAD.format(project_id=project_id, file_id=file_id)

    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Utworzono folder: {folder}")

    try:
        # Pobieranie nazwy pliku
        with urllib.request.urlopen(url_info) as response:
            data = json.load(response)
            fileName = data['data']['fileName']

        # Pobieranie pliku
        destination = os.path.join(folder, fileName)
        with urllib.request.urlopen(url_download) as response:
            total_file_size = int(response.headers.get("Content-Length", 0))

            with open(destination, "w+b") as out_file:
                downloaded_file_size = 0
                start_time = time.time()

                for data in response:
                    out_file.write(data)

                    downloaded_file_size += len(data)
                    elapsed_time = time.time() - start_time
                    speed = (downloaded_file_size / 1024) / elapsed_time if elapsed_time > 0 else 0

                    progress_bar_downloading(downloaded_file_size, total_file_size, speed, elapsed_time, prefix=f'[{fileNumber}/{totalNumber}]', suffix=f'{fileName}   ')

                out_file.flush()
                os.fsync(out_file.fileno())

        print(f"-  Pobrano pomyślnie")

    except urllib.error.HTTPError as e:
        print(f"Błąd HTTP: {e.code}")
    except urllib.error.URLError as e:
        print(f"Błąd URL: {e.reason}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def download_ModrinthMOD(url_download, path, fileNumber, totalNumber, folder="mods"):
    fileName = path.split("/")[-1]
    path_folder = os.path.dirname(path)
    final_folder = os.path.join(folder, path_folder)

    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(final_folder):
        os.makedirs(final_folder)
        print(f"Utworzono folder: {final_folder}")

    try:
        # Pobieranie pliku
        destination = os.path.join(final_folder, fileName)
        with urllib.request.urlopen(url_download) as response:
            total_file_size = int(response.headers.get("Content-Length", 0))

            with open(destination, "w+b") as out_file:
                downloaded_file_size = 0
                start_time = time.time()

                for data in response:
                    out_file.write(data)

                    downloaded_file_size += len(data)
                    elapsed_time = time.time() - start_time
                    speed = (downloaded_file_size / 1024) / elapsed_time if elapsed_time > 0 else 0

                    progress_bar_downloading(downloaded_file_size, total_file_size, speed, elapsed_time, prefix=f'[{fileNumber}/{totalNumber}]', suffix=f'{fileName}   ')

                out_file.flush()
                os.fsync(out_file.fileno())

        print(f"-  Pobrano pomyślnie")

    except urllib.error.HTTPError as e:
        print(f"Błąd HTTP: {e.code}")
    except urllib.error.URLError as e:
        print(f"Błąd URL: {e.reason}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def unZIP(zip_file_path, folder_name):

    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Utworzono folder: {folder_name}")

    # Rozpakowanie pliku .zip
    try:
        extract_to = os.path.join(os.getcwd(), folder_name)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            total_files = len(file_list)

            start_time = time.time()

            for i, file in enumerate(file_list, 1):
                zip_ref.extract(file, extract_to)

                elapsed_time = time.time() - start_time
                speed = i / elapsed_time if elapsed_time > 0 else 0

                progress_bar_unzipping(i, total_files, speed, elapsed_time, prefix='Rozpakowywanie')
    
        print(f"-  Rozpakowano pomyślnie")

    except FileNotFoundError:
        print(f"Błąd: Plik '{zip_file_path}' nie został znaleziony.")
    except zipfile.BadZipFile:
        print(f"Błąd: Plik '{zip_file_path}' jest uszkodzony lub nie jest poprawnym plikiem ZIP.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

def loadJsonFile(json_file_path):

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print(f"Błąd: Plik '{json_file_path}' nie został znaleziony.")
    except json.JSONDecodeError:
        print("Błąd: Plik JSON jest niepoprawnie sformatowany.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
    
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download mods for modpack")
    parser.add_argument("file", help="Path to .zip / .mrpack file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--curseforge", action="store_true", help="Flag for downloading mods from CurseForge")
    group.add_argument("--modrinth", action="store_true", help="Flag for downloading mods from Modrinth")

    args = parser.parse_args()
    file_path = args.file
    folder_name = os.path.splitext(os.path.basename(file_path))[0]

    if args.curseforge:
        unZIP(file_path, folder_name)
        json_file_path = f'{folder_name}/manifest.json'
        manifestData = loadJsonFile(json_file_path)

        if "files" in manifestData:
            total_files = len(manifestData["files"])
            for index, file_entry in enumerate(manifestData["files"], start=1):
                project_id = int(file_entry.get("projectID", 0))
                file_id = int(file_entry.get("fileID", 0))
                required = file_entry.get("required", False)
                download_CurseForgeMOD(project_id, file_id, index, total_files, f"{folder_name}/overrides")
        else:
            print("Brak sekcji 'files' w JSON.")
    elif args.modrinth:
        #zip_path = file_path.replace('.mrpack', '.zip')
        zip_path = file_path.rsplit('.', 1)[0] + ".zip"
        shutil.copy2(file_path, zip_path)
        #os.rename(file_path, zip_path)
        unZIP(zip_path, folder_name)
        json_file_path = f'{folder_name}/modrinth.index.json'
        manifestData = loadJsonFile(json_file_path)
        if "files" in manifestData:
            total_files = len(manifestData["files"])
            for index, file_entry in enumerate(manifestData["files"], start=1):
                path = file_entry.get("path", "")
                downloads = file_entry.get("downloads", [])

                if downloads:
                    download_url = downloads[0]
                    if not os.path.isabs(path):
                        download_ModrinthMOD(download_url, path, index, total_files, f"{folder_name}/overrides")
        else:
            print("Brak sekcji 'files' w JSON.")
    else:
        print("No flag provided. Proceeding without downloading from CurseForge or Modrinth.")

    