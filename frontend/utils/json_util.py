import os
import json
from datetime import datetime

DEFAULTS_DIR = "defaults"


def save_defaults_to_timestamped_file(data, dir_path=DEFAULTS_DIR):
    os.makedirs(dir_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    path = os.path.join(dir_path, f"default_{timestamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path


def list_default_files(dir_path=DEFAULTS_DIR):
    os.makedirs(dir_path, exist_ok=True)
    return sorted(
        [f for f in os.listdir(dir_path) if f.endswith(".json")],
        reverse=True  # 最新的在上面
    )


def load_defaults_from_file(filename, dir_path=DEFAULTS_DIR):
    path = os.path.join(dir_path, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
