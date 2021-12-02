FROM debian:11.1

RUN apt update && apt install -y python3 python3-pip \
                                 git \
                                 vim \
                                 cmake \
                                 libjpeg-dev \
                                 g++ \
                                 build-essential \
                                 libfreetype6-dev \
                                 dirmngr \
                                 gnupg \
                                 libx11-dev \
                                 apt-transport-https \
                                 software-properties-common \
                                 ca-certificates \
                                 cloc \
                                 curl && \
                                 rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/mowshon/age-and-gender.git /tmp/age-and-gender && \
    cd /tmp/age-and-gender && \
    python3 setup.py install && \
    rm -Rf /tmp/age-and-gender && \
    python3 -c "from age_and_gender import *" || exit 1

#RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list && \
#    curl -sSL https://www.mongodb.org/static/pgp/server-5.0.asc -o mongoserver.asc && \
#    gpg --no-default-keyring --keyring ./mongo_key_temp.gpg --import ./mongoserver.asc && \
#    gpg --no-default-keyring --keyring ./mongo_key_temp.gpg --export > ./mongoserver_key.gpg && \
#    mv mongoserver_key.gpg /etc/apt/trusted.gpg.d/ && \
#    apt update && apt install -y --no-install-recommends mongodb-org-shell \
#                                                         mongodb-database-tools && \
#                                                         rm -rf /var/lib/apt/lists/*

RUN adduser --quiet \
            --disabled-password \
            --shell /bin/bash \
            --home /home/user \
            --gecos '' user

WORKDIR /home/user
USER user

RUN git clone https://github.com/itomilin/data_analysis.git -b develop

