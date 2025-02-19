import zipfile
import time
import json
import os

from progressBar import progress_bar_unzipping

def unZIP(zip_file_path, folder_name):

    # Creating folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder created: {folder_name}")

    # Extracting .zip file
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

                progress_bar_unzipping(i, total_files, speed, elapsed_time, prefix='Extracting')
    
        print(f"-  Successfully extracted")

    except FileNotFoundError:
        print(f"Error: File '{zip_file_path}' not found.")
    except zipfile.BadZipFile:
        print(f"Error: The file '{zip_file_path}' is either corrupted or not a valid ZIP file.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def loadJsonFile(json_file_path):

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print("Error: The JSON file is improperly formatted.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None