import zipfile
import os

def zip_folder(folder_path: str, zip_name: str) -> str:
    zip_path = f"{zip_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                z.write(full_path, os.path.relpath(full_path, folder_path))

    return zip_path
