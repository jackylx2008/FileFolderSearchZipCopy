import os
import shutil

import INIT
from FileFolderSearch import FileSearch, PatternMaker

CNCC2_ROOT = INIT.CloudStation_ROOT + r"国会二期/"
DESIGN_DOCX_ROOT = INIT.CloudStation_ROOT + r"Python/Project/DesignChange_Doc/B25B26/"
DESKTOP_ROOT = INIT.Desktop_ROOT
BIAD_folder_obj = INIT.BIAD_folder_obj
Decoration_folder_obj = INIT.Decoration_folder_obj
BIAD_file_obj = INIT.BIAD_file_obj
Decoration_file_obj = INIT.Decoration_file_obj
CNCC2_file_obj = INIT.CNCC2_file_obj
Design_docx_obj = INIT.Design_docx_obj


def copy_files_to_destination(file_paths, destination_dir):
    """
    Copy files from the given list of absolute file paths to a destination directory.

    Args:
    - file_paths (list): A list containing absolute paths of files to be copied.
    - destination_dir (str): The absolute path of the destination directory.

    Returns:
    - None

    This function copies files specified in the file_paths list to the destination directory.
    """
    # Check if the destination directory exists, if not, create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Loop through the list of file paths and copy them to the destination directory
    for file_path in file_paths:
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(destination_dir, file_name)

            try:
                shutil.copy(file_path, destination_path)
                print(f"File '{file_name}' copied successfully to '{destination_dir}'.")
            except PermissionError:
                print(
                    f"Permission denied to copy '{file_name}' to '{destination_dir}'."
                )
            # Optionally, you might want to handle other exceptions based on your requirements
        else:
            print(f"File '{file_path}' does not exist.")


def copy_pdf_or_docx_to_desk(
    docx_src: str, folder: FileSearch, destination_path: str, file_type: str
) -> list:
    """Copy PDF or DOCX files related to DesignChange numbers from a source folder to a destination folder.

    Args:
        docx_src (str): Source directory containing .docx files.
        folder (FileSearch): Object representing the folder to search for <file_type> files.
        destination_path (str): Destination directory where PDF files will be copied.
        file_type (str): Which type files to copy, pdf or docx

    Returns:
        list: A list of DesignChange numbers found in the .docx files.
    """
    DesignChange_num = []
    # Get pattern for searching
    p = PatternMaker("2526all").get_pattern()

    # Find docx files based on the pattern
    docx_list = FileSearch(docx_src).find_files_with_extension_and_pattern("docx", p)

    # Extract relevant parts from docx filenames to collect DesignChange numbers
    for docx in docx_list:
        docx_parts = docx.split(" ")[0].split(r"/")[-1]
        DesignChange_num.append(docx_parts)

    try:
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
    except Exception:
        print("Cannot make dir")
        return []
    # Find corresponding PDF files based on DesignChange numbers
    for keyword in DesignChange_num:
        files_list = folder.find_files_with_extension_and_keyword(file_type, keyword)
        if files_list:
            if len(files_list) == 1:
                copy_files_to_destination(files_list, destination_path)
            else:
                raise ValueError("More than one file to copy")
        else:
            raise ValueError(
                "List is empty. Cannot perform operation with an empty list."
            )

    return DesignChange_num


if __name__ == "__main__":
    # test_get_last_change_num()
    new_folder = DESKTOP_ROOT + "1111/"
    DesignChange_num = copy_pdf_or_docx_to_desk(
        DESIGN_DOCX_ROOT, CNCC2_file_obj, new_folder, "pdf"
    )
    DesignChange_num = copy_pdf_or_docx_to_desk(
        DESIGN_DOCX_ROOT, Design_docx_obj, new_folder, "docx"
    )
    for num in DesignChange_num:
        print(num)
