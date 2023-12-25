import os

path = "D:/CloudStation/国会二期/12 主体精装/主体精装变更/集美暖通/06-03-C2-V001 (排烟口改普通风口)/"

# 删除路径末尾的斜杠（如果有的话）并获取最后一个文件夹名
last_folder = [folder for folder in path.rstrip("/").split("/") if folder][-1]
print(f"最后一个文件夹名字: {last_folder}")
