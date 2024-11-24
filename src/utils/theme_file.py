import json
import os

THEMES_FILE_PATH = "./utils/themes.json"

def load_themes():
    """
    Load theme settings from a JSON file.
    If the file does not exist, return the default settings.
    """
    if os.path.exists(THEMES_FILE_PATH):
        with open(THEMES_FILE_PATH, 'r') as file:
            themes = json.load(file)
            return themes
    else:
        # Default themes if the file doesn't exist
        return {
            "Outdoor": (100, 50),
            "Indoor": (50, 10)
        }

def save_themes(themes):
    """
    Save theme settings to a JSON file.
    """
    os.makedirs(os.path.dirname(THEMES_FILE_PATH), exist_ok=True)
    with open(THEMES_FILE_PATH, 'w') as file:
        json.dump(themes, file, indent=4)
