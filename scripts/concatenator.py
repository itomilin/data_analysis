#!/usr/bin/python3.9

import argparse
import pathlib
import json


def concatenated_info(path):
    path_to_storage_file = path
    with open(path_to_storage_file, 'r') as f:
        data = f.read()

    storage_info = json.loads(data)
    size_kbytes = int(storage_info["total_downloads_kbytes"])
    seconds = int(storage_info["elapsed_time_seconds"])
    id_list = storage_info["id_repositories"]

    return size_kbytes, seconds, id_list


def write_to_file(out_file, sizet, sect, id_lt):
    json_obj = {}
    json_obj["total_downloads_kbytes"] = sizet
    json_obj["elapsed_time_seconds"] = sect
    json_obj["id_repositories"] = id_lt

    with open(out_file, 'w') as f:
        json.dump(json_obj, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-p", "--path",
                        dest="path",
                        help="Path to dir structure.",
                        required=True)
    parser.add_argument("-o", "--out_file",
                        dest="out_file",
                        help="Path to output file.",
                        required=True)

    args = parser.parse_args()

    files = sorted(pathlib.Path(args.path).glob('**/parsed_info.json'))

    size_total = 0
    sec_total = 0
    id_l_total = []
    for file in files:
        size, sec, id_l = concatenated_info(file)
        size_total += size
        sec_total += sec
        id_l_total += id_l
    write_to_file(args.out_file, size_total, sec_total, id_l_total)
    print(f"<<<Done>>>\n"
          f"Scanned {len(files)} files.\n"
          f"Check in {args.out_file}\n"
          f"Total:\nSIZE: {size_total}\nSECONDS: {sec_total}\nREPO_COUNT: {len(id_l_total)}")

