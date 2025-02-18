import urllib.request
import json
import zipfile
import shutil
import time
import sys
import os

URL_CURSEFORGE_INFO = "https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}"
URL_CURSEFORGE_DOWNLOAD = "https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}/download"

def progress_bar_downloading(iteration, total, speed, elapsed_time, prefix='', suffix='', bar_length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = fill * filled_length + '-' * (bar_length - filled_length)

    downloaded_mb = iteration / (1024 * 1024)
    total_mb = total / (1024 * 1024)

    sys.stdout.write(f'\r{prefix:<10} [{downloaded_mb:.2f}MB/{total_mb:.2f}MB  {speed:.2f}kB/s  {elapsed_time:.2f}s] |{bar}| {percent}% - {suffix}')
    sys.stdout.flush()

def progress_bar_unzipping(iteration, total, speed, elapsed_time, prefix='', suffix='', bar_length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = fill * filled_length + '-' * (bar_length - filled_length)

    if speed >= 1024:
        speed_display = f"{speed / 1024:.2f} MB/s"
    else:
        speed_display = f"{speed:.2f} kB/s"
    
    minutes, seconds = divmod(elapsed_time, 60)
    elapsed_formatted = f"{int(minutes)}m {int(seconds)}s" if minutes > 0 else f"{elapsed_time:.2f}s"

    sys.stdout.write(f'\r{prefix:<12} [{iteration}/{total}] {percent}% |{bar}| {speed_display}  {elapsed_formatted}     {suffix}')
    sys.stdout.flush()

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

                    progress_bar_downloading(downloaded_file_size, total_file_size, speed, elapsed_time, prefix=f'[{fileNumber}/{totalNumber}]', suffix=f'{fileName}')

                out_file.flush()
                os.fsync(out_file.fileno())

        print(f"  -  Pobrano pomyślnie")

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
    zip_file_path = 'TFCH-1.5.5b.zip'
    folder_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    unZIP(zip_file_path, folder_name)

    json_file_path = f'{folder_name}/manifest.json'
    manifestData = loadJsonFile(json_file_path)
    print(manifestData)