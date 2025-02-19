import urllib.request
import json
import time
import os

from progressBar import progress_bar_downloading

URL_CURSEFORGE_INFO = "https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}"
URL_CURSEFORGE_DOWNLOAD = "https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}/download"

def download_CurseForgeMOD(project_id, file_id, fileNumber, totalNumber, folder="mods"):
    url_info = URL_CURSEFORGE_INFO.format(project_id=project_id, file_id=file_id)
    url_download = URL_CURSEFORGE_DOWNLOAD.format(project_id=project_id, file_id=file_id)

    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Folder created: {folder}")

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

        print(f"-  Downloaded successfully")
        return True

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code}")
        return False
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def download_ModrinthMOD(url_download, path, fileNumber, totalNumber, folder="mods"):
    fileName = path.split("/")[-1]
    path_folder = os.path.dirname(path)
    final_folder = os.path.join(folder, path_folder)

    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(final_folder):
        os.makedirs(final_folder)
        print(f"Folder created: {final_folder}")

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

        print(f"-  Downloaded successfully")
        return True

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code}")
        return False
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False