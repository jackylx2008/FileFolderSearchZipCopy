import os
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


# pattern = PatternMaker.set_all_pattern().get_pattern()
#
# input_txt = "./csv_txt/lists.txt"
output_txt = "./csv_txt/temp.txt"
# pre_proc_txt(input_txt, output_txt)
# remove_chinese_characters(output_txt)
#
# match_str_list = get_strings_matching_pattern(output_txt, pattern)

# Read the file and store each line in a list
with open(output_txt, "r") as file:
    match_str_list = [line.strip() for line in file]
size_match_str = len(match_str_list)

print(match_str_list)
for str in match_str_list:
    print(str)

# Step2: Zip the folders to Desktop
is_B25B26 = True
is_B24 = False
new_folder = INIT.Desktop_ROOT + "1111/"
if is_B24:
    try:
        B24 = [
            INIT.CNCC2_ROOT + "12 北京院-B24地块/酒店设计变更/酒店给排水/",
            INIT.CNCC2_ROOT + "12 北京院-B24地块/酒店设计变更/酒店暖通/",
        ]
        match_list_list = []
        for folder in B24:
            temp_list = FolderSearch(folder).find_folders_with_keyword_list(
                match_str_list
            )
            match_list_list.append(temp_list)

        for list in match_list_list:
            for folder in list:
                ZipFolder.zip_folder(folder, new_folder)
    except IndexError:
        print("IndexError: match_list is empty")

if is_B25B26:
    try:
        B25B26 = [
            INIT.CNCC2_ROOT + "12 北京院-主体/415设计变更/415给排水/",
            INIT.CNCC2_ROOT + "12 北京院-主体/415设计变更/415暖通/",
            INIT.CNCC2_ROOT + "12 主体精装/主体精装变更/",
        ]
        match_list_list = []
        for folder in B25B26:
            temp_list = FolderSearch(folder).find_folders_with_keyword_list(
                match_str_list
            )
            match_list_list.append(temp_list)

        for list in match_list_list:
            for folder in list:
                ZipFolder.zip_folder(folder, new_folder)
    except IndexError:
        print("IndexError: match_list is empty")

# Setp3: Make sure all zip files
numbers_zip = 0
for i, file in enumerate(os.listdir(new_folder), start=1):
    # Check if the file ends with .zip extension
    if file.endswith(".zip"):
        numbers_zip = numbers_zip + 1
        print(f"{i}. {file}")

print(f"Got {size_match_str} changes to zip")
print(f"Got {numbers_zip} in {new_folder}")
