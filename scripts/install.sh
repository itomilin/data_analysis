#!/bin/bash

uid=$(id -u)
if [ $uid -ne 0 ]; then
    echo "Please use sudo or run the script as root."
    exit 1
fi

# base.
apt install git vim

# age-and-gender deps.
apt install cmake \
            libjpeg-dev \
            g++ \
            build-essential \
            libfreetype6-dev \
            dirmngr \
            gnupg \
            apt-transport-https \
            software-properties-common \
            ca-certificates \
            curl

python3 -c "from age_and_gender import *"
if [[ $? == 0 ]]; then
    printf "%s\n" "DNN python lib already installed."
else
    git clone git@github.com:mowshon/age-and-gender.git /tmp/age-and-gender
    cd age-and-gender
    python3 setup.py install
    rm -Rf /tmp/age-and-gender
fi

if [[ -z `which cloc` ]]; then
    apt install -y cloc
else
    printf "<<%s>>\n" "Cloc already installed."
fi


if [[ -z `which mongo` ]]; then
    echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
    curl -sSL https://www.mongodb.org/static/pgp/server-5.0.asc -o mongoserver.asc
    gpg --no-default-keyring --keyring ./mongo_key_temp.gpg --import ./mongoserver.asc
    gpg --no-default-keyring --keyring ./mongo_key_temp.gpg --export > ./mongoserver_key.gpg
    mv mongoserver_key.gpg /etc/apt/trusted.gpg.d/

    apt update && \
    apt install -y \
                --no-install-recommends \
                mongodb-org-shell \
                mongodb-database-tools
else
    printf "<<%s>>\n" "Mongodb shell N tools already installed."
fi

