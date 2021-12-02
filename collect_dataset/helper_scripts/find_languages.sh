#!/bin/bash

PATH_TO_REPO=$1

if [[ -z $PATH_TO_REPO ]]; then
    echo "[ ERROR ] Path to repository is not set!"
    exit 1
fi

out=`cloc --quiet --hide-rate --exclude-lang='C++','C/C++ Header' --csv \
    $PATH_TO_REPO 2> /dev/null | head -n -1 | \
    awk -F ',' 'NR > 2 { printf "%s;%s\n", $2, $1 }'`

printf "%s\n" $out

