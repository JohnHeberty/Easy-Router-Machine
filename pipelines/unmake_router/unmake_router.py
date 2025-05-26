import shutil
import os

if __name__ == "__main__":

    print("Unmaking router...")

    path_data = os.path.join("data","external")
    # Lista apenas as pastas dentro de path_data
    folders = [f for f in os.listdir(path_data) if os.path.isdir(os.path.join(path_data, f))]
    # Deleta todas as pastas dentro de folders
    for folder in folders:
        folder_path = os.path.join(path_data, folder)
        print("REMOVING FOLDER:",folder_path)
        # shutil.rmtree(folder_path, ignore_errors=False, onerror=None)

    path_data = os.path.join("data","processed")
    # Lista apenas as pastas dentro de path_data
    folders = [f for f in os.listdir(path_data) if os.path.isdir(os.path.join(path_data, f))]
    # Deleta todas as pastas dentro de folders
    for folder in folders:
        folder_path = os.path.join(path_data, folder)
        print("REMOVING FOLDER:",folder_path)
        # shutil.rmtree(folder_path, ignore_errors=False, onerror=None)
