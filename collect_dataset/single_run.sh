#!/bin/bash -e

LOGIN=$1
TOKEN=$2
# Ex. /home/big_data/mongodb_documents
ROOT_DOCS=$3
# Year 2010-2020
YEAR=$4
# Workdir, for download github_avatars and repos. For each instance must be
# different.
WORKDIR=$5

if [[ -z $LOGIN ]] || [[ -z $TOKEN ]] || [[ -z $ROOT_DOCS ]] || [[ -z $YEAR ]] || [[ -z $WORKDIR ]]; then
    echo "Wrong args."
    echo -e "LOGIN\nTOKEN\nROOT_DOCS\nYEAR\nWORKDIR"
    exit 1;
fi

cd ./collect_dataset

#
for month_num in {1..12}
do
    ./main.py -t $TOKEN \
              -l $LOGIN \
              -d $ROOT_DOCS/$YEAR/$month_num/ \
              -i $ROOT_DOCS/$YEAR/$month_num/parsed_info.json \
              -w $WORKDIR \
              -s ${YEAR}-${month_num}-1
done

