#!/bin/bash -e

if [[ -z `which mongoimport` ]]; then
    printf "<<%s>>\n" "mongoimport not found."
    exit 1
fi

PATH=$1
if [[ -z $PATH ]]; then
    printf "<<%s>>\n" "PATH to directory with documents is not set."
    exit 1
fi

/usr/bin/find $PATH -type f \
                    -name "document_*.json" \
                    -exec /usr/bin/mongoimport \
                          --username=root \
                          --password=rootpassword \
                          --host=localhost \
                          --port=27017 \
                          --authenticationDatabase="admin" \
                          --db=my_big_data \
                          --collection=github_repos \
                          --file={} \;

