#!/bin/bash -e

PATH_TO_REPO=$1

if [[ -z $PATH_TO_REPO ]]; then
    echo "[ ERROR ] Path to repository is not set!"
    exit 1
fi

# For src and headers (empty, comments and code).
summarize_cpp=`cloc --quiet --hide-rate --csv --include-lang='C++','C/C++ Header' $PATH_TO_REPO |& tail -n 1`
# For everything (empty, comments and code).
summarize_all=`cloc --quiet --hide-rate --csv $PATH_TO_REPO |& tail -n 1`

total_lines_cpp=`echo $summarize_cpp | awk -F ',' '{ print $3 + $4 + $5 }'`
total_files_cpp=`echo $summarize_cpp | awk -F ',' '{ print $1 }'`

total_lines_another=`echo $summarize_all | awk -F ',' '{ print $3 + $4 + $5 }'`
total_files_another=`echo $summarize_all | awk -F ',' '{ print $1 }'`

echo -e "lines_cpp;${total_lines_cpp}\nfiles_cpp;${total_files_cpp}\n`
        `lines_another;${total_lines_another}\nfiles_another;${total_files_another}"

