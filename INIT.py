from FileFolderSearch import FileSearch, FolderSearch, Which_OS

which_os = Which_OS()
CloudStation_ROOT = which_os.get_CloudStation_root() + r"CloudStation/"
Desktop_ROOT = which_os.get_desktop()
# d = "~/CloudStation/国会二期/37 厨房顾问/主体厨房/主体厨房变更/"

CNCC2_ROOT = CloudStation_ROOT + r"国会二期/"
DESIGN_DOCX_ROOT = CloudStation_ROOT + r"Python/Project/DesignChange_Doc/B25B26/"
BIAD_folder_obj = FolderSearch(CNCC2_ROOT + "12 北京院-主体/415设计变更/")
Design_docx_obj = FileSearch(DESIGN_DOCX_ROOT)
Decoration_folder_obj = FolderSearch(CNCC2_ROOT + "12 主体精装/主体精装变更/")
Gas_folder_obj = FolderSearch(CNCC2_ROOT + "05 市政条件/燃气集团/主体燃气设计变更/")
Power_folder_obj = FolderSearch(CNCC2_ROOT + "05 市政条件/热力集团/主体热力设计变更/")
Kitchen_folder_obj = FolderSearch(CNCC2_ROOT + "37 厨房顾问/主体厨房/主体厨房变更/")
B25B26_folder_list = [
    BIAD_folder_obj,
    Decoration_folder_obj,
    Gas_folder_obj,
    Kitchen_folder_obj,
]
B25B26_folder_dict = {
    "biad": BIAD_folder_obj,
    "decoration": Decoration_folder_obj,
    "gas": Gas_folder_obj,
    "kithen": Kitchen_folder_obj,
}


BIAD_file_obj = FileSearch(CNCC2_ROOT + "12 北京院-主体/415设计变更/")
Decoration_file_obj = FileSearch(CNCC2_ROOT + "12 主体精装/主体精装变更/")
CNCC2_file_obj = FileSearch(CNCC2_ROOT)
pattern_biad_05_E = {"first": "05", "second": "E"}
pattern_biad_05_C = {"first": "05", "second": "C"}
pattern_biad_06_E = {"first": "06", "second": "E"}
pattern_biad_06_C = {"first": "06", "second": "C"}
pattern_biad_list = [
    pattern_biad_06_C,
    pattern_biad_06_E,
    pattern_biad_05_C,
    pattern_biad_05_E,
]
pattern_decoration_O5_V = {"first": "05", "second": "V"}
pattern_decoration_O5_B = {"first": "05", "second": "B"}
pattern_decoration_O6_V = {"first": "06", "second": "V"}
pattern_decoration_O6_B = {"first": "06", "second": "B"}

pattern_decoration_list = [
    pattern_decoration_O5_V,
    pattern_decoration_O5_B,
    pattern_decoration_O6_V,
    pattern_decoration_O6_B,
]
