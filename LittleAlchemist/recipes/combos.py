import json
import glob

def get_all_combos():
    files_list = [f for f in glob.glob("recipes/*.json")]
    file_names = [name.replace(".json", "") for name in files_list]

    all_combos = {}

    for i, f in enumerate(files_list):
        with open(f) as json_file:
            data = json.load(json_file)
            all_combos[file_names[i].replace("recipes\\", "")] = data

    return all_combos
