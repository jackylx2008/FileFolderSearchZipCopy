import re


def find_pattern_in_string(input_string):
    pattern = r"\d{2}-\d{2}-[A-Z]\d-[A-Z0-9]{3}"
    matches = re.findall(pattern, input_string)
    return matches


# 测试字符串
file_path = "D:/CloudStation/Python/Project/DesignChange_Doc/B25B26/05-03-C2-V001 (L2L3修改走廊天花形式).docx"

found_parts = find_pattern_in_string(file_path)
print(found_parts)
