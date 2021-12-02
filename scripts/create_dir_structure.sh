#!/bin/bash -e

BASE_DIR=$1
# Path to tamplate file parsed_info.json (this storage at project root)
PATH_TO_PARSED_JSON=$2

if [[ -z $BASE_DIR ]] || [[ -z $PATH_TO_PARSED_JSON ]]; then
    printf "%s\n" "[ ERROR ] BASE_DIR is not set || PATH_TO_PARSED_JSON!"
    exit 1
fi

MONGO_DOCS_PATH=/$BASE_DIR/dataset
mkdir $MONGO_DOCS_PATH

# For each decade.
for year in {2010..2020}
do
    for month_num in {1..12}
    do
        mkdir -p $MONGO_DOCS_PATH/${year}/${month_num}
        cp $PATH_TO_PARSED_JSON $MONGO_DOCS_PATH/${year}/${month_num}
    done
done

# For each decade.
for year in {2020..2021}
do
    for month_num in {1..12}
    do
        mkdir -p $MONGO_DOCS_PATH/${year}/${month_num}
        cp $PATH_TO_PARSED_JSON $MONGO_DOCS_PATH/${year}/${month_num}
    done
done

