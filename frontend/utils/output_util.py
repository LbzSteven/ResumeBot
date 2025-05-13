import os
from datetime import datetime


def save_output_to_file(content, dir_path="output"):
    os.makedirs(dir_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = ("output_" + timestamp + ".txt")
    file_path = os.path.join(dir_path, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path
