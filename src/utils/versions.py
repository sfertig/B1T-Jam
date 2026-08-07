import os
import sys
import platform
import json

from ..VERSION import VERSION

######################
## DEFAULTS
######################

SETTINGS = {
    "version": VERSION
}
SAVE_DATA = {
    "created": False,
    "version": VERSION
}


def get_save_dir_path() -> str:
    """Stores save data in C:/Users/<Username>/.tearfultilling_saveData"""
    user_home = os.path.expanduser("~")
    return os.path.join(user_home, ".tearfultilling_saveData")


def init_save_dir():
    
    path = get_save_dir_path()
    exists = os.path.exists(path)
    
    # 1. Safe folder creation
    os.makedirs(path, exist_ok=True)

    # 2. Helper function to safely write a JSON file only if it doesn't exist
    def create_json_if_missing(file_name: str, default_data: dict):
        file_path = os.path.join(path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump(default_data, f, indent=4)

    # 3. Create actual JSON files with initial defaults
    create_json_if_missing("settings.json", SETTINGS)
    create_json_if_missing("save_1.json", SAVE_DATA)
    create_json_if_missing("save_2.json", SAVE_DATA)
    create_json_if_missing("save_3.json", SAVE_DATA)

    if not exists: print(f"[SaveSystem] Save directory initialized at: {path}")
    else: print(f"[SaveSystem] Save directory already exists at: {path}")
    print(f"path: {path}")