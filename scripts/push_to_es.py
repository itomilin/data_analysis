#!/usr/bin/python3.9

import pathlib
import argparse
import requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-p", "--path",
                        dest="path",
                        help="Path to dir structure. Ex. '/home/big_data/dataset/'",
                        required=True)
    args = parser.parse_args()

    # "/home/big_data/dataset/"
    path = args.path

    if path[-1] != '/':
        print("[ ERROR ] Path must be ended '/' symbol.")
        exit(1)

    p = pathlib.Path(path)
    files = sorted(p.glob('**/document_*.json'))

    counter = 0
    for file in files:
        with open(file, 'r') as f:
            data = f.read()

        url = f'http://localhost:9200/big_data/_doc/{counter}'
        payload = open(file)
        headers = {'content-type': 'application/json',
                   'Accept-Charset': 'UTF-8'}
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print(f"[ OK ] Doc {file} added to {url}")
        counter += 1

