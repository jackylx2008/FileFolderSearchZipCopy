import os
import platform
import re


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

    def fine_folders_with_keyword_list(self, keyword_list) -> list:
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
            for folder_path, _, folders in os.walk(root_path):
                for folder in folders:
                    for keyword in keyword_list:
                        if keyword in folder:
                            matching_folders.append(os.path.join(folder_path, folder))
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
