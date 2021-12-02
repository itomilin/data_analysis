# data_analysis

# Collect dataset
- Host way
1) download git repo & cd to downloaded folder
2) install deps ```./scripts/install.sh```
3) ```./scripts/create_dir_structure.sh /home/big_data/ ./scripts/parsed_info.json```
4) ```./collect_dataset/single_run.sh <git_login> <git_token> <path_to_dataset_structure> <year_git_api> <tmp_workdir>```
- Docker way
1) download git repo & cd to downloaded folder
2) ```./scripts/create_dir_structure.sh /home/big_data/ ./scripts/parsed_info.json```
3) ```cd ./docker``` and run ```./build_image.sh``` after build run ```./run_docker.sh```
4) Inside docker, download git repo & cd to downloaded folder
5) ```./collect_dataset/single_run.sh <git_login> <git_token> <path_to_dataset_structure> <year_git_api> <tmp_workdir>```
6) ```./collect_dataset/single_run.sh <git_login> <git_token> <path_to_dataset_structure> <year_git_api> <tmp_workdir>```

# Get statistics (if dataset already collected)
1) Download git repo & cd to downloaded folder
2) unpack dataset arch ```tar xf ./dataset.tar.gz```
3) Run elastic with ```docker-compose -f ./docker/docker-compose.yml up -d es```
4) Check that es is up ```./elastic/check_index.sh``` and w8, if out is ```curl: (7) Failed to connect to localhost port 9200: Connection refused``` or ```curl: (56) Recv failure: Connection reset by peer``` just w8 some time
5) Create index ```./elastic/create_index.sh```
6) Upload dataset to elastic ```./scripts/push_to_es.py -p ./dataset/```
7) After upload all data, visualise it with ```cd ./elastic``` && ```./generate_plots.py``` all plots located to ./elastic/plots/

