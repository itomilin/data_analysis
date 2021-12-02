#!/bin/bash

PATH_TO_REPO=$1
FILE_FOR_SEARCH=$2

if [[ -z $PATH_TO_REPO ]]; then
    echo "[ ERROR ] Path to repository is not set!"
    exit 1
fi

extensions=( "*.c++" "*.c" "*.cpp" "*.cc" "*.cxx" )

total_spaces=0
total_tabs=0

for ext in ${extensions[@]}
do
    tabs=`find $PATH_TO_REPO -type f -iname $ext -exec grep -Pc "^\t+\w" {} \; | awk '{ n += $1 }; END { print n }'`
    four_spaces=`find $PATH_TO_REPO -type f -iname $ext -exec grep -Pc "^\ {4}\w" {} \; | awk '{ n += $1 }; END { print n }'`

    total_spaces=$(( total_spaces + four_spaces ))
    total_tabs=$(( total_tabs + tabs ))
done

echo -e "tabs;${total_tabs}\nspaces;${total_spaces}"

