#!/usr/bin/python3.9

import argparse
import pendulum
from searching.github_request import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-t", "--api_token",
                        dest="api_token",
                        help="Github API token.",
                        required=True)
    parser.add_argument("-l", "--login",
                        dest="login",
                        help="Github login.",
                        required=True)
    parser.add_argument("-d", "--json_docs_path",
                        dest="json_docs",
                        help="Path to json-docs storage directory.",
                        required=True)
    parser.add_argument("-i", "--info_file",
                        dest="summary_info",
                        help="Path to json-based info file.",
                        required=True)
    parser.add_argument("-w", "--workdir",
                        dest="workdir",
                        help="Path to workdir directory.",
                        required=True)
    parser.add_argument("-s", "--start_date",
                        dest="start_date",
                        help="Month for interval.",
                        required=True)

    args = parser.parse_args()
    start_date = None
    start = None
    end = None
    try:
        start_date = datetime.strptime(args.start_date,
                                       "%Y-%m-%d").date()
        dt = pendulum.datetime(start_date.year, start_date.month,
                               start_date.day)
        start = dt.start_of('month')
        end = dt.end_of('month')
    except ValueError:
        print("Wrong date format. must be YYYY-MM-DD")
        exit(1)

    if not os.path.isdir(args.json_docs):
        print(f"Directory is not exist {args.json_docs}")
        exit(1)

    if not os.path.isfile(args.summary_info):
        print(f"File is not exist {args.summary_info}")
        exit(1)

    # Call data collect. github_request.py
    run_collect_dataset(args.login,
                        args.api_token,
                        args.json_docs,
                        args.summary_info,
                        args.workdir,
                        start,
                        end)

    print("<<<<<<<<<<DONE>>>>>>>>>>")

