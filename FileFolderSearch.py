import os
import platform
import re
import shutil
from datetime import datetime


class PatternMaker:
    """
    Generates a pattern based on company-specific criteria.
    """

    def __init__(self, which_company: str, replace_word_dict: dict) -> None:
        """
        Initializes a PatternMaker object with company-specific parameters.

        Args:
        - which_company (str): The name of the company.
        - replace_word_dict (dict): Dictionary containing 'first' and 'second' keys.
        """
        self._which_company = which_company
        self._pattern = r""
        self._replace_word_dict = replace_word_dict

    @classmethod
    def set_biad_all(cls):
        return cls(which_company="biad", replace_word_dict=dict())

    @classmethod
    def set_all_pattern(cls):
        return cls(which_company="all", replace_word_dict=dict())

    def get_pattern(self) -> str:
        """
        Generates and returns a pattern based on the specified company's criteria.

        Returns:
        - str: The generated pattern.
        Raises:
        - KeyError: If 'first' or 'second' keys are missing in the dictionary.
        """
        if self._which_company == "biad" and self._replace_word_dict:
            try:
                self._pattern = (
                    r"("
                    + self._replace_word_dict["first"]
                    + r")"
                    + r"(-\d{2}-C\d{1}-0\d{2}-)("
                    + self._replace_word_dict["second"]
                    + r")"
                )
            except KeyError:
                raise KeyError("Key 'first' or 'second' is missing in the dictionary")
        elif self._which_company == "biad" and not self._replace_word_dict:
            self._pattern = (
                r"(" + r"d{2}" + r")" + r"(-\d{2}-C\d{1}-0\d{2}-)(" + r"[A-Z]" + r")"
            )
        elif self._which_company == "decoration":
            try:
                self._pattern = (
                    r"("
                    + self._replace_word_dict["first"]
                    + r")"
                    + r"(-\d{2}-C\d{1}-"
                    + self._replace_word_dict["second"]
                    + r"0\d{2})"
                )
            except KeyError:
                raise KeyError("Key 'first' or 'second' is missing in the dictionary")
        elif self._which_company == "all":
            try:
                # self._pattern = r"\d{2}-\d{2}-[A-Z]\d-[A-Z0-9]{4}"
                self._pattern = r"\b\d{2}-\d{2}-[A-Z]\d-(?:V\d{3}|\d{3}-[A-Z])\b"
            except KeyError:
                raise KeyError("Key 'first' or 'second' is missing in the dictionary")

        return self._pattern


class FileSearch:
    """
    Provides methods to search for files within a specified folder based on keywords and extensions.
    """

    def __init__(self, folder_path: str) -> None:
        """
        Initializes a FileSearch object with the specified folder path.

        Args:
        - folder_path (str): The path of the folder to search for files.
        """
        self.folder_path = folder_path
        self._pattern = ""

    def find_files_with_keyword(self, keyword) -> list:
        """
        Finds files within the folder containing a specific keyword.

        Args:
        - keyword (str): The keyword to search for in the file names.

        Returns:
        - list: A list of file paths that contain the specified keyword.
        """
        # Traverse all files in the folder
        file_list = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                # Match the keyword
                if keyword in file:
                    file_list.append(os.path.join(root, file).replace("\\", "/"))
        return file_list

    def find_files_with_extension_and_keyword(self, extension, keyword) -> list:
        """
        Finds files within the folder matching a specific extension and containing a keyword.

        Args:
        - extension (str): The file extension to filter by (e.g., '.txt', '.csv').
        - keyword (str): The keyword to search for in the file names.

        Returns:
        - list: A list of file paths that match the specified extension and contain the keyword.
        """
        # Traverse all files in the folder
        file_list = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                # Check file extension and match the keyword
                if file.endswith(extension) and keyword in file:
                    file_list.append(os.path.join(root, file).replace("\\", "/"))
        return file_list

    def find_files_with_extension_and_pattern(self, extension, pattern) -> list:
        """
        Finds files within the folder matching a specific extension and containing a pattern.

        Args:
        - extension (str): The file extension to filter by (e.g., '.txt', '.csv').
        - pattern (str): The pattern to search for in the file names.

        Returns:
        - list: A list of file paths that match the specified extension and pattern.
        """
        # Traverse all files in the folder
        file_list = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                # Check file extension and match the pattern
                if file.endswith(extension) and re.findall(pattern, file):
                    full_file_path = os.path.join(root, file).replace("\\", "/")
                    file_list.append(full_file_path)
        return file_list


class FolderSearch:
    """
    Provides methods to search for folders within a specified path based on a pattern.
    """

    def __init__(self, target_path: str) -> None:
        """
        Initializes a FolderSearch object with the specified target path.

        Args:
        - target_path (str): The path in which folders will be searched.
        """
        self._target_path = target_path

    def is_folder_created_on_date(self, target_date: str):
        try:
            # Get the creation time of the folder
            creation_time = os.path.getctime(self._target_path)

            # Convert the creation time to a datetime object
            creation_date = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d")

            # Compare the creation date with the target date
            return creation_date == target_date
        except FileNotFoundError:
            print(f"Folder '{self._target_path}' not found.")
            return False

    def find_folders_with_pattern(self, pattern) -> list:
        """
        Finds folders within the target path matching a specific pattern.

        Args:
        - pattern (str): The pattern to search for in the folder names.

        Returns:
        - list: A list of folder paths that match the specified pattern.
        """
        matching_folders = []
        try:
            if not pattern:
                raise ValueError("ERROR: Pattern string is empty")
            else:
                root_path = self._target_path
                for root, dirs, _ in os.walk(root_path):
                    for d in dirs:
                        if re.findall(pattern, d):
                            path = os.path.join(root, d)
                            path = path.replace("\\", "/")
                            matching_folders.append(path)
                    # matching_folders.extend( [os.path.join(root, d) for d in dirs if re.findall(pattern, d)])
                matching_folders.sort()
        except ValueError as e:
            print(e)
        return matching_folders

    def find_folders_with_keyword_list(self, keyword_list) -> list:
        """
        Search for folders containing any of the specified keywords within the given root folder.

        Args:
        - keyword_list (list): A list of keywords to search for within folder names.

        Returns:
        - list: A list containing paths of folders that contain any of the specified keywords in their names.
        """
        matching_folders = []

        try:
            # Check if keyword_list is empty
            if not keyword_list:
                raise ValueError("Empty keyword_list provided")

            # Walk through the directory tree starting from the root_folder
            root_path = self._target_path
            for dirpath, dirnames, _ in os.walk(root_path):
                for folder in dirnames:
                    for keyword in keyword_list:
                        if keyword in folder:
                            matching_folders.append(
                                os.path.join(dirpath, folder).replace("\\", "/") + "/"
                            )
                            break  # Stop checking other keywords for this folder

        except ValueError as e:
            print(e)  # Print the error message if keyword_list is empty
            return []  # Return an empty list

        return matching_folders


class Which_OS:
    """
    Provides methods to retrieve information about the operating system.
    """

    def __init__(self) -> None:
        # Using platform.system()
        os_name = platform.system()
        self._CloudStation_root = ""
        self._Desktop = ""
        self._os_name = ""
        userhome = ""
        if os_name == "Darwin":
            self._CloudStation_root = r"/Users/liuxin/"
            userhome = os.path.expanduser("~")
            self._os_name = "mac"
        elif os_name == "Windows":
            self._CloudStation_root = r"D:/"
            # username = getpass.getuser()
            userhome = os.path.expanduser("~").replace(r"\\", r"/")
            self._os_name = "windows"
        self._Desktop = f"{userhome}/Desktop/"

    def get_CloudStation_root(self):
        """
        Retrieves the CloudStation root path based on the operating system.

        Returns:
        - str: The CloudStation root path.
        """
        return self._CloudStation_root

    def get_os_name(self):
        """
        Retrieves the name of the operating system.

        Returns:
        - str: The name of the operating system ('mac' or 'windows').
        """
        return self._os_name

    def get_desktop(self):
        return self._Desktop


class FolderUtility:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.dir_list = []

    def replace_parentheses(self):
        # 遍历指定目录下的文件夹
        for root, dirs, _ in os.walk(self.directory_path):
            for dir_name in dirs:
                # 构建文件夹的完整路径
                dir_path = os.path.join(root, dir_name)

                # 替换括号
                new_dir_name = dir_name.replace("（", " (").replace("）", ")")

                # 构建新的文件夹路径
                new_dir_path = os.path.join(root, new_dir_name)

                # 重命名文件夹
                os.rename(dir_path, new_dir_path)
                print(f"Renamed: {dir_path} -> {new_dir_path}")

    def traverse(self, level=1):
        if not os.path.isdir(self.directory_path):
            print(f"{self.directory_path} 不是一个有效的目录路径")
            return

        self._traverse_directory_helper(self.directory_path, 0, level)
        return self.dir_list

    def _traverse_directory_helper(self, current_path, current_level, target_level):
        if current_level > target_level:
            return

        files_and_folders = [
            f
            for f in os.listdir(current_path)
            if os.path.isdir(os.path.join(current_path, f))
        ]

        for item in files_and_folders:
            item_path = os.path.join(current_path, item)
            if current_level + 1 <= target_level:
                if os.path.isdir(item_path):
                    # print(f"{'  ' * current_level}[Folder] {item}")
                    self.dir_list.append(item_path.replace("\\", "/"))
                    self._traverse_directory_helper(
                        item_path, current_level + 1, target_level
                    )
                # else:
                # print(f"{'  ' * current_level}[File] {item}")

    def traverse_one_level(self, type="dir"):
        dir_list = []
        try:
            # List all items in the directory
            items = os.listdir(self.directory_path)

            for item in items:
                # Construct the full path of the item
                item_path = os.path.join(self.directory_path, item)

                # Check if it is a file or a subdirectory
                if os.path.isfile(item_path):
                    if type == "file":
                        dir_list.append(item_path.replace("\\", "/"))
                        print(f"File: {item}")
                elif os.path.isdir(item_path):
                    if type == "dir":
                        dir_list.append(item_path.replace("\\", "/"))
                else:
                    print(f"Unknown: {item}")
            return dir_list

        except OSError as e:
            print(f"Error: {e}")

    @staticmethod
    def remove_directory(directory_path):
        try:
            shutil.rmtree(directory_path)
            # print(f"Directory '{directory_path}' successfully removed.")
        except Exception as e:
            print(f"Error while removing directory '{directory_path}': {e}")

    def copy_to_upper_dir(self):
        try:
            # Extract the parent dir path
            parent_dir = os.path.dirname(self.directory_path)

            # Specify the destination path
            dest_dir = parent_dir

            CloudStation_ROOT = Which_OS().get_CloudStation_root() + r"CloudStation/"
            temp_dir = CloudStation_ROOT + "temp"
            # Copy the contents of the source dir to temp
            shutil.copytree(self.directory_path, temp_dir)
            self.remove_directory(parent_dir)
            shutil.copytree(temp_dir, dest_dir)
            self.remove_directory(temp_dir)

            print(
                f"Contents of '{self.directory_path}' successfully copied to '{dest_dir}'."
            )
            return True
        except Exception as e:
            print(f"Error while copying contents: {e}")
            return False


def CopyToUpperDir(directory_path=r"C:\Users\bcjt_\Desktop\新建文件夹"):
    dir_level_1_list = FolderUtility(directory_path).traverse_one_level()
    try:
        for d1 in dir_level_1_list:
            dir_level_2_list = FolderUtility(d1).traverse_one_level()
            for d2 in dir_level_2_list:
                if os.path.basename(d2)[:14] == os.path.basename(d1)[:14]:
                    if FolderUtility(d2).copy_to_upper_dir():
                        # FolderUtility.remove_directory(d2)
                        print(d2 + "Copied!")
        FolderUtility(directory_path).replace_parentheses()

    except ValueError as e:
        print(e)


# Only for BIAD
def CheckSubDirNameAndSet(
    directory_path=r"C:\Users\bcjt_\Desktop\新建文件夹", dir_name="word&cad"
):
    dir_1_list = FolderUtility(directory_path).traverse_one_level()
    for d1 in dir_1_list:
        dir_2_list = FolderUtility(d1).traverse_one_level(type="dir")
        for d2 in dir_2_list:
            # if dir_name not in d2:
            last_folder_name = os.path.basename(d2)
            if last_folder_name != dir_name:
                print(d2)
                # os.rename(d2, d1 + "/" + "word&cad")


def ChangeSubDirName():
    directory_path = r"D:\CloudStation\国会二期\12 北京院-主体\415设计变更"
    level2 = FolderUtility(directory_path).traverse(2)
    level1 = FolderUtility(directory_path).traverse(1)
    result = []
    for item in level2:
        if item not in level1:
            result.append(item)
    for p in result:
        CheckSubDirNameAndSet(p)


if __name__ == "__main__":
    directory_path = r"D:\CloudStation\国会二期\12 北京院-主体\415设计变更"
    level3 = FolderUtility(directory_path).traverse(3)
    level2 = FolderUtility(directory_path).traverse(2)
    level1 = FolderUtility(directory_path).traverse(1)
    result = []
    for item in level3:
        if item not in level1 and item not in level2:
            result.append(item)
    for p in result:
        if FolderSearch(p).is_folder_created_on_date("2024-02-04"):
            print(p)
