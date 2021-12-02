#!/bin/bash

docker run --rm \
            -it \
            -v /home/big_data/dataset:/home/user/dataset \
            collect_dataset:1.0.0 /bin/bash

