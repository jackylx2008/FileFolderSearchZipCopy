import re

import INIT
import ZipFolder
from FileFolderSearch import FolderSearch, PatternMaker


# Step1: Read txt to get change's num
def pre_proc_txt(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Replace all occurrences of "、" with ","
        modified_content = content.replace("、", ",")

        # Write the modified content to a new file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(modified_content)

        print(f"Replacement completed. Modified content saved to '{output_file}'")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")


def remove_chinese_characters(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Remove Chinese characters using regex
        cleaned_content = re.sub("[\u4e00-\u9fff]+", "", content)
        cleaned_content = re.sub("[\uff00-\uffef]+", "", cleaned_content)

        # Write the cleaned content back to the same file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(cleaned_content)

        print("Chinese characters removed. File updated successfully.")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")


def get_strings_matching_pattern(file_path, pattern):
    matched_strings = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                matches = re.findall(pattern, line)
                matched_strings.extend(matches)
    except FileNotFoundError:
        print("File not found or path is incorrect.")

    return matched_strings


pattern = PatternMaker("2526biad").get_pattern()

input_txt = "./csv_txt/lists.txt"
output_txt = "./csv_txt/temp.txt"
pre_proc_txt(input_txt, output_txt)
remove_chinese_characters(output_txt)

match_str_list = get_strings_matching_pattern(output_txt, pattern)
size_match_str = len(match_str_list)
print(f"Got {size_match_str} changes to zip")
for str in match_str_list:
    print(str)

# Step2: Zip the folders to Desktop
new_folder = INIT.Desktop_ROOT + "1111/"
try:
    match_list = FolderSearch(INIT.CNCC2_ROOT).find_folders_with_keyword_list(
        match_str_list
    )
    for folder in match_list:
        ZipFolder.zip_folder(folder, new_folder)
except IndexError:
    print("IndexError: match_list is empty")
