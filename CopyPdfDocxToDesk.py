import os
import re
import shutil

import INIT
from FileFolderSearch import FileSearch, FolderSearch, PatternMaker

CNCC2_ROOT = INIT.CloudStation_ROOT + r"国会二期/"
DESIGN_DOCX_B25B26 = INIT.CloudStation_ROOT + r"Python/Project/DesignChange_Doc/B25B26/"
DESIGN_DOCX_B24 = INIT.CloudStation_ROOT + r"Python/Project/DesignChange_Doc/B24/"
DESKTOP_ROOT = INIT.Desktop_ROOT
BIAD_folder_obj = INIT.BIAD_folder_obj
Decoration_folder_obj = INIT.Decoration_folder_obj
BIAD_file_obj = INIT.BIAD_file_obj
Decoration_file_obj = INIT.Decoration_file_obj
CNCC2_file_obj = INIT.CNCC2_file_obj
Design_docx_obj = INIT.Design_docx_obj


def test_get_last_change_num():
    def get_last_change_num(
        folder: FolderSearch, pattern_list: list, which_company: str
    ):
        for pattern in pattern_list:
            p = PatternMaker(which_company, pattern)
            try:
                match_list = folder.find_folders_with_pattern(p.get_pattern())
                last_change = match_list[-1]
                last_change_num = last_change.split("\\")[-1]
                print(last_change_num)
            except IndexError:
                print("IndexError: match_list is empty")

    get_last_change_num(BIAD_folder_obj, INIT.pattern_biad_list, "biad")
    get_last_change_num(
        Decoration_folder_obj, INIT.pattern_decoration_list, "decoration"
    )


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
    p = PatternMaker("all", dict()).get_pattern()

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
                for pdf_file in files_list:
                    print(pdf_file + "More than one file to copy")
                raise ValueError("More than one file to copy")
        else:
            print(file_type)
            print(keyword + "   ValueError")
            raise ValueError(
                "List is empty. Cannot perform operation with an empty list."
            )

    return DesignChange_num


def copy_pdf_docx_to_desk(
    docx_src: str, pdf_folder: str, destination_dir: str, split_str: str
):
    DesignChange_num = []
    for design_change_docx in os.listdir(docx_src):
        if design_change_docx.endswith("docx"):
            DesignChange_num.append(design_change_docx.split(split_str)[0])
    docx = FileSearch(docx_src).find_files_with_keyword("docx")
    pdf = []
    for num in DesignChange_num:
        pdf_list = FileSearch(pdf_folder).find_files_with_extension_and_keyword(
            "pdf", num
        )
        for p in pdf_list:
            pdf.append(p)
    # print(docx)
    # print(pdf)

    try:
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)
    except Exception:
        print("Cannot make dir")
        return
    if len(docx) != len(pdf):
        for num in DesignChange_num:
            pdf_count = 0
            for p in pdf:
                if num in p:
                    pdf_count = pdf_count + 1

            if pdf_count != 1:
                print(f"{num} have more than one pdf")
                return
    else:
        copy_files_to_destination(docx, destination_dir)
        copy_files_to_destination(pdf, destination_dir)


def copy_pdf_docx_B25B26_biad():
    # test_get_last_change_num()
    new_folder = DESKTOP_ROOT + "1111/"
    DesignChange_num = copy_pdf_or_docx_to_desk(
        DESIGN_DOCX_B25B26, CNCC2_file_obj, new_folder, "pdf"
    )
    DesignChange_num = copy_pdf_or_docx_to_desk(
        DESIGN_DOCX_B25B26, Design_docx_obj, new_folder, "docx"
    )
    for num in DesignChange_num:
        print(num)


def copy_pdf_docx_B24():
    copy_pdf_docx_to_desk(
        DESIGN_DOCX_B24,
        CNCC2_ROOT + "12 北京院-B24地块/酒店设计变更/",
        DESKTOP_ROOT + "1111/",
        "（",
    )


def copy_pdf_docx_B25B26_V2():
    copy_pdf_docx_to_desk(
        DESIGN_DOCX_B25B26,
        CNCC2_ROOT + "12 主体精装/主体精装变更/",
        DESKTOP_ROOT + "1111/",
        " ",
    )


if __name__ == "__main__":
    # copy_pdf_docx_B25B26_biad()
    # copy_pdf_docx_B25B26_V2() # WARN: Do not work
    copy_pdf_docx_B24()
