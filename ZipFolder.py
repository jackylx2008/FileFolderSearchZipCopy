import os
import zipfile

import INIT
from FileFolderSearch import PatternMaker


def zip_folder(folder_path, destination_path=None):
    """
    Compresses the contents of a folder into a zip file named after the folder itself.

    Args:
    - folder_path (str): The path of the folder to be zipped.
    - destination_path (str, optional): The path where the zip file will be saved. If None, it saves in the current directory.
    """
    try:
        if destination_path is None:
            destination_path = os.path.dirname(folder_path)

        last_folder = [
            folder for folder in folder_path.rstrip("/").split("/") if folder
        ][-1]
        output_zip = os.path.join(destination_path, last_folder + ".zip")
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))
        print(f"Folder '{folder_path}' zipped successfully as '{output_zip}'")
    except Exception as e:
        print(f"Error zipping folder: {e}")


def test_zip_folder():
    new_folder = INIT.Desktop_ROOT + "1111/"
    print(new_folder)

    p = PatternMaker("2526biad")
    try:
        match_list = INIT.BIAD_folder_obj.find_folders_with_pattern(p.get_pattern())
        for file in match_list:
            zip_folder(file, new_folder)
    except IndexError:
        print("IndexError: match_list is empty")


# Example usage:
# zip_folder('/path/to/source_folder', '/path/to/destination_folder')
