#!/usr/bin/env python3
import os
import shutil
import json
import sys

from random_json import generate_random_json

default_nb_json = 50
nb_json = default_nb_json

if len(sys.argv) >= 2:
    nb_json = int(sys.argv[1])


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))

    data_folder = f"{dir_path}/data"
    access_rights = 0o755

    if os.path.isdir(data_folder):
        shutil.rmtree(data_folder)
        print('"data" folder detected and removed')

    os.mkdir(data_folder, access_rights)
    print('"data" folder created \n')

    for i in range(nb_json):
        with open(f"data/{i}.json", "w") as f:
            obj = json.dumps(generate_random_json(), indent=4)
            f.write(obj)
            print(f'File "{i}.json" created (length of {len(obj)})')

