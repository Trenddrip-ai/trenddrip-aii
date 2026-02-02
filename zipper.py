import os
import zipfile
from datetime import datetime


def zip_collection(output_folder: str) -> str:
    """
    Zips a finished TrendDrip collection folder into a single file.
    Returns the zip file name.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    zip_name = f"TrendDrip_Collection_{timestamp}.zip"
    zip_path = os.path.join(os.getcwd(), zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_folder)
                zipf.write(full_path, arcname)

    return zip_name
