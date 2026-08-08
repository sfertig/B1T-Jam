import os
import sys
import platform
import json

from ..VERSION import VERSION

######################
## DEFAULTS
######################

SETTINGS = {
    "version": VERSION,
    "modified": False,
    "fps": 60,
    "title": "Tearful Tilling"
}
SAVE_DATA = {
    "created": False,
    "modified": False,
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

def update_dict_defaults(user_data: dict, default_data: dict) -> dict:
    """
    Returns a new dict containing all latest default keys, 
    overwritten by any existing user values.
    """
    if not user_data["modified"]: return default_data.copy() #uder never adjusted values, they use system defaults
    # Start with a full copy of the latest defaults
    updated = default_data.copy()
    
    # Overwrite defaults with whatever keys the user already has saved
    updated.update(user_data)
    #overwrite version
    updated["version"] = VERSION
    
    return updated

def load_settings():
    path = os.path.join(get_save_dir_path(), "settings.json")
    with open(path, "r") as f: data = json.load(f)
    data = update_dict_defaults(data, SETTINGS)
    save_settings(data)
    return data

def load_save_file(index: int):
    path = os.path.join(get_save_dir_path(), f"save_{index}.json")
    with open(path, "r") as f: data = json.load(f)
    data = update_dict_defaults(data, SAVE_DATA)
    save_save_file(index, data)
    return data

def save_settings(data):
    path = os.path.join(get_save_dir_path(), "settings.json")
    with open(path, "w") as f: json.dump(data, f, indent=4)
def save_save_file(index: int, data):
    path = os.path.join(get_save_dir_path(), f"save_{index}.json")
    with open(path, "w") as f: json.dump(data, f, indent=4)
    