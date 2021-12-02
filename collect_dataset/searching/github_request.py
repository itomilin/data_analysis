from datetime import datetime, timedelta
import time

import requests
import os
import git
import shutil
import json
import csv
from subprocess import run, check_output

from age_and_gender import *
from PIL import Image

import github
from github import GithubException


def image_detection(avatars_urls, workdir_path):
    data = AgeAndGender()
    shape_predictor = "./searching/data/shape" \
                      "_predictor_5_face_landmarks.dat"
    gender_classifier = "./searching/data/dnn_gender_classifier_v1.dat"
    data.load_shape_predictor(shape_predictor)
    data.load_dnn_gender_classifier(gender_classifier)

    recognized_avatars = []
    path_to_image = f"{workdir_path}/github_avatar.jpg"
    for avatar_url in avatars_urls:
        with open(path_to_image, 'wb') as handle:
            response = requests.get(avatar_url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        img = Image.open(path_to_image).convert("RGB")
        result = data.predict(img)

        if os.path.exists(path_to_image):
            os.remove(path_to_image)
        else:
            print(f"The {path_to_image} does not exist.")

        if not result:
            recognized_avatars.append("NO_DATA")
        else:
            gender = result[0]['gender']['value']
            recognized_avatars.append(gender.upper())
    return recognized_avatars


class JsonBuilder:
    def __init__(self, downloaded_repo_path, github_repo_id):
        # Path to downloaded github project repo.
        self._repo_path = downloaded_repo_path
        # For json document (nosql bd).
        self._github_repo_id = github_repo_id
        # Create a json object.
        self._json_obj = {}

    def write_to_json(self, json_docs_path):
        path = json_docs_path
        filename = f'document_{self._github_repo_id}.json'
        # Write the object to file.
        with open(path + filename, 'w') as f:
            json.dump(self._json_obj, f, indent=4, sort_keys=True)

    def set_full_name(self, full_name):
        self._json_obj['full_name'] = full_name

    def set_created_date(self, created):
        self._json_obj['created_at'] = created

    def set_updated_date(self, updated):
        self._json_obj['updated_at'] = updated

    def set_dockerfile(self, script_name):
        # https://csatlas.com/python-subprocess-run-stdout-stderr/
        cmd = run([script_name, self._repo_path, "Dockerfile"], capture_output=True)
        self._json_obj['dockerfile'] = json.loads(cmd.stdout.decode().replace('\n', '').lower())

    def set_readme(self, script_name):
        cmd = run([script_name, self._repo_path, "README.md"], capture_output=True)
        self._json_obj['readme'] = json.loads(cmd.stdout.decode().replace('\n', '').lower())

    def set_license(self, repository_license):
        if not repository_license:
            self._json_obj['license'] = "NO_DATA"
        else:
            self._json_obj['license'] = repository_license

    def set_branches(self, branches):
        self._json_obj['branches'] = branches

    def set_contributors(self, total_count, male, female, unrecognized):
        self._json_obj['contributors_total_count'] = total_count
        self._json_obj['contributors_male'] = male
        self._json_obj['contributors_female'] = female
        self._json_obj['contributors_unrecognized'] = unrecognized

    def set_lines_of_code(self, script_name):
        cmd = run([script_name, self._repo_path], capture_output=True)
        reader = csv.reader(cmd.stdout.decode().splitlines(), delimiter=';')
        lines_n_files = list(reader)  # Ex. [['lines_cpp', '512908'], ['files_cpp', '2444'], ['lines_another', '930294'], ['files_another', '5192']]
        self._json_obj['cpp_src_lines'] = int(lines_n_files[0][1])
        self._json_obj['cpp_src_files'] = int(lines_n_files[1][1])
        self._json_obj['another_files'] = int(lines_n_files[2][1])
        self._json_obj['all_lines'] = int(lines_n_files[3][1])

    def set_another_languages(self, script_name):
        self._json_obj['another_languages'] = []
        cmd = run([script_name, self._repo_path], capture_output=True)
        reader = csv.reader(cmd.stdout.decode().splitlines(),
                            delimiter=';')
        for item in reader:
            try:
                self._json_obj['another_languages'].append({
                    f'name': item[0],
                    f'count': int(item[1])
                })
            # Could raise if out equal ['Bourne'] ['Again'] ['Shell', '33'] ['DOS']
            except IndexError:
                pass

    def set_build_system(self, script_name):
        self._json_obj['build_system'] = []

        cmake = run([script_name, self._repo_path, "CMakeLists.txt"], capture_output=True)
        qmake = run([script_name, self._repo_path, "*.pro"], capture_output=True)
        meson = run([script_name, self._repo_path, "meson.build"], capture_output=True)
        make = run([script_name, self._repo_path, "Makefile"], capture_output=True)
        ms_build = run([script_name, self._repo_path, "*.sln"],
                       capture_output=True)

        self._json_obj['build_system'].append({
            'cmake': json.loads(cmake.stdout.decode().replace('\n', '').lower())
        })

        self._json_obj['build_system'].append({
            'qmake': json.loads(qmake.stdout.decode().replace('\n', '').lower())
        })

        self._json_obj['build_system'].append({
            'meson': json.loads(meson.stdout.decode().replace('\n', '').lower())
        })

        self._json_obj['build_system'].append({
            'make': json.loads(make.stdout.decode().replace('\n', '').lower())
        })

        self._json_obj['build_system'].append({
            'ms_build': json.loads(
                ms_build.stdout.decode().replace('\n', '').lower())
        })

    def set_indents(self, script_name):
        command = run([script_name, self._repo_path], capture_output=True)
        reader = csv.reader(command.stdout.decode().splitlines(), delimiter=';')
        indents = list(reader)  # Ex. [['tabs', '0'], ['spaces', '176']]
        tabs = int(indents[0][1])
        spaces = int(indents[1][1])
        self._json_obj['count_tabs'] = tabs
        self._json_obj['count_spaces'] = spaces
        if tabs > spaces:
            self._json_obj['indention_method_dominate'] = "tab"
        else:
            self._json_obj['indention_method_dominate'] = "space"
        if tabs == 0:
            self._json_obj['indention_method'] = "space"
        elif spaces == 0:
            self._json_obj['indention_method'] = "tab"
        elif tabs > 0 and spaces > 0:
            self._json_obj['indention_method'] = "mixed"

    def set_issues(self, total_count, open_count, close_count, issue_titles):
        self._json_obj['issues_open'] = open_count
        self._json_obj['issues_close'] = close_count
        self._json_obj['total_issues'] = total_count
        self._json_obj['issue_titles'] = issue_titles

    def set_fork_count(self, fork_count):
        self._json_obj['forks'] = fork_count

    def set_star_count(self, star_count):
        self._json_obj['stars'] = star_count

    def set_description(self, description):
        if not description:
            self._json_obj['description'] = "NO_DATA"
        else:
            self._json_obj['description'] = description


def get_data(repository_json_object, downloaded_repo_path, repo_id,
             session, json_docs_path, workdir_path):
    json_builder = JsonBuilder(downloaded_repo_path, repo_id)
    full_name = repository_json_object["full_name"]
    star_count = repository_json_object["stargazers_count"]
    forks_count = repository_json_object["forks_count"]
    created_date = repository_json_object["created_at"]
    updated_date = repository_json_object["updated_at"]
    description = repository_json_object["description"]

    branches_url = f"https://api.github.com/repos/{full_name}/branches"
    branches = []
    for branch in session.get(branches_url).json():
        branches.append(branch["name"])
    json_builder.set_branches(branches)

    contributors_url = repository_json_object["contributors_url"]
    avatars_urls = []
    for page in range(1, 100):
        query = f"?per_page=100&page={page}"
        contributors = session.get(contributors_url + query).json()
        if len(contributors) != 0:
            for contributor in contributors:
                avatars_urls.append(contributor["avatar_url"])
        else:
            break

    # Check issues.
    count_open_issues = 0
    count_close_issues = 0
    issues_url = f"https://api.github.com/repos/{full_name}/issues"
    issues_titles = []
    # Limit 1000 issues.
    for page in range(1, 11):
        open_issues_query = f"?state=all&per_page=100&page={page}"
        issues = session.get(issues_url + open_issues_query).json()

        if not issues:
            break

        for issue in issues:
            issue_title = issue["title"]
            issue_state = issue["state"]
            issues_titles.append(issue_title)
            if issue_state == "open":
                count_open_issues += 1
            elif issue_state == "closed":
                count_close_issues += 1
    count_issues = len(issues_titles)

    recognized_avatars = image_detection(avatars_urls, workdir_path)
    total_count = len(recognized_avatars)
    men_count = recognized_avatars.count("MALE")
    women_counts = recognized_avatars.count("FEMALE")
    unrecognized_count = recognized_avatars.count("NO_DATA")

    # Fill object for creating a json document.
    json_builder.set_full_name(full_name)
    json_builder.set_created_date(created_date)
    json_builder.set_updated_date(updated_date)
    json_builder.set_dockerfile("./helper_scripts/find_file.sh")
    json_builder.set_readme("./helper_scripts/find_file.sh")
    if repository_json_object["license"] is None:
        repository_license = None
    else:
        repository_license = repository_json_object["license"]["name"]
    json_builder.set_license(repository_license)
    json_builder.set_branches(branches)
    json_builder.set_contributors(male=men_count,
                                  female=women_counts,
                                  total_count=total_count,
                                  unrecognized=unrecognized_count)
    try:
        json_builder.set_lines_of_code("./helper_scripts/calculate_lines_count.sh")
    except ValueError:
        return False
    json_builder.set_another_languages("./helper_scripts/find_languages.sh")
    json_builder.set_build_system("./helper_scripts/find_file.sh")
    json_builder.set_indents("./helper_scripts/tab_space_analysis.sh")
    json_builder.set_issues(total_count=count_issues,
                            open_count=count_open_issues,
                            close_count=count_close_issues,
                            issue_titles=issues_titles)
    json_builder.set_fork_count(forks_count)
    json_builder.set_star_count(star_count)
    json_builder.set_description(description)
    json_builder.write_to_json(json_docs_path)
    return True


def update_parsed_info(file, size_mb, repository_id, elapsed_time):
    path_to_storage_file = file
    with open(path_to_storage_file, 'r') as f:
        data = f.read()

    storage_info = json.loads(data)

    if repository_id not in storage_info["id_repositories"]:
        storage_info["total_downloads_kbytes"] += size_mb
        storage_info["elapsed_time_seconds"] += int(elapsed_time)
        storage_info["id_repositories"].append(repository_id)
        json_data = json.dumps(storage_info,
                               ensure_ascii=False,
                               indent=4)
        with open(path_to_storage_file, 'w', encoding='utf-8') as f:
            f.write(json_data)
        return True
    else:
        return False


def is_repository_exist(repository_id, file):
    path_to_storage_file = file
    with open(path_to_storage_file, 'r') as f:
        data = f.read()
    storage_info = json.loads(data)
    if repository_id in storage_info["id_repositories"]:
        return True
    else:
        return False


def get_dir_size(path):
    size = check_output(['du', '-s', path]).split()[0].decode('utf-8')
    return int(size)


def print_debug_info(counter, full_name, repository_id, api_limit=None):
    if api_limit is None:
        return f"<< Repo number: {counter}\t" \
               f"\tName {full_name}" \
               f"\tID: {repository_id} >>"
    else:
        return f"<< Repo number: {counter}\t" \
               f"\tName {full_name}" \
               f"\tID: {repository_id}" \
               f"\tLimit_used: {api_limit} of 5000 >>"


def check_github_api_limit(response):
    limit_used = int(response.headers["x-ratelimit-used"])
    limit_limit = int(response.headers["x-ratelimit-limit"])
    limit_reset = int(response.headers["x-ratelimit-reset"])
    dt_obj = datetime.fromtimestamp(limit_reset)

    if limit_limit == 5000 and limit_used > 4300:
        print(f"<<<<Critical limit per repo. Wait until {dt_obj}>>>>")
        while limit_reset > int(datetime.now().timestamp()):
            time.sleep(1)

    if response.status_code == 403:
        print(f"<<<<Current {limit_used}. Wait until {dt_obj}>>>>")
        while limit_reset > int(datetime.now().timestamp()):
            time.sleep(1)
        time.sleep(2)  # To be sure than api make it updated.
    elif response.status_code == 401:
        print(response.text)
        print("\n\n!!Wrong credentials!!\nCheck o_auth.")
        exit(1)
    return limit_used


def is_repo_empty(full_name, github_token):
    g = github.Github(github_token)
    repo = g.get_repo(full_name)

    try:
        # get repo content from root directory
        repo.get_contents("/")
    except GithubException as e:
        return True  # output: This repository is empty.
    except requests.exceptions.ReadTimeout as e2:
        return True
    except requests.exceptions.ConnectTimeout as e3:
        return True
    return False


def download_git_repo(full_name, path):
    git.Repo.clone_from(f"https://github.com/{full_name}.git",
                        path,
                        depth=1)


def run_collect_dataset(login, token, json_docs_path, summary_info_path,
                        workdir, start_date, end_date):
    delta = timedelta(days=1)  # Interval for date.
    counter = 0
    url = "https://api.github.com/search/repositories"

    session = requests.Session()
    session.auth = (login, token)
    # Date.
    while start_date <= end_date:
        q_date = start_date.strftime("%Y-%m-%d")
        # Page.
        for page_num in range(1, 11):
            # ?per_page=100&page=1&q=language:cpp+created:2010-12-27
            query = f"?per_page=100&page={page_num}&" \
                    f"q=language:cpp+created:{q_date}"
            response = session.get(url + query)

            if response.status_code == 403:
                check_github_api_limit(response)
                response = session.get(url + query)

            repositories = None
            try:
                repositories = response.json()["items"]
            # If list empty, then repo is ended.
                if not repositories:
                    break
            except json.decoder.JSONDecodeError:
                print(f"[ ERROR ] Decoding err, skipping {url}{query}")
            total_repo_per_day = json.loads(response.text)['total_count']
            print(f"Total repo: {len(repositories)} | Repo per day:"
                  f" {total_repo_per_day} | " + url + query)
            # Items.
            for repository in repositories:
                perf_s = datetime.now()
                counter += 1
                # Skip if repo is fork.
                if repository["fork"]:
                    html_repo = repository["html_url"]
                    print(f"Repo {html_repo} is fork, skipping.")
                    continue
                repo_id = repository["id"]
                path = f"{workdir}/{repo_id}"
                full_name = repository["full_name"]
                # Проверяем, если id есть в json, тогда пропускаем.
                if not is_repository_exist(repo_id, summary_info_path):
                    # If rate close to limit, wait until reset.
                    response = session.get("https://api.github.com/users/itomilin")
                    api_used_repo = check_github_api_limit(response)
                    print(print_debug_info(counter, full_name, repo_id,
                                           api_used_repo))
                    # Клонируем.
                    try:
                        download_git_repo(full_name, path)
                    except git.exc.GitCommandError as e:
                        if e.status == 128:
                            print(e.stderr)
                            shutil.rmtree(path)
                            print("Repo already exist, download again.")
                            download_git_repo(full_name, path)

                    # Собираем json документ для mongodb.
                    # Проверяем если репозиторий пустой, то пропускаем.
                    ret_val = False
                    if not is_repo_empty(full_name, token):
                        ret_val = get_data(repository, path, repo_id,
                                           session, json_docs_path, workdir)
                    else:
                        print('[ ERROR ] Repo is empty skipping...')

                    if ret_val:
                        dir_size = get_dir_size(path)
                    else:
                        dir_size = 0
                    perf_e = datetime.now()
                    elapsed_seconds = (perf_e - perf_s).total_seconds()
                    print("**elapsed_seconds: " + str(elapsed_seconds))
                    # Обновляем json с данными.
                    update_parsed_info(summary_info_path, dir_size,
                                       repo_id, elapsed_seconds)
                    # Удаляем загруженный репозиторий.
                    try:
                        shutil.rmtree(path)
                    except:
                        print('Error deleting directory')
                else:
                    print(print_debug_info(counter, full_name, repo_id))
        start_date += delta

