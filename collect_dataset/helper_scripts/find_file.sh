#!/bin/bash

PATH_TO_REPO=$1
FILE_FOR_SEARCH=$2

if [[ -z $PATH_TO_REPO ]] || [[ -z $FILE_FOR_SEARCH ]]; then
    echo "[ ERROR ] Path to repository || file is not set!"
    exit 1
fi

file=`find $PATH_TO_REPO -type f -iname "$FILE_FOR_SEARCH"`

# Return python style bool.
if [[ -z $file ]]; then
    echo "False"
else
    echo "True"
fi

