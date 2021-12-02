#TODO
#!/bin/bash -e

LOGIN=$1
TOKEN=$2

if [[ -z $LOGIN ]] || [[ -z $TOKEN ]]; then
    echo "Wrong args."
    exit 1;
fi

Y2010_01_mongodb_docs=$HOME/mongodb_documents/2010_01
touch $Y2010_01_mongodb_docs/parsed_info_2010_01.json
mkdir -p $Y2010_01_mongodb_docs
./main.py -t $TOKEN \
          -l $LOGIN \
          -d $Y2010_01_mongodb_docs \
          -i $Y2010_01_mongodb_docs/parsed_info_2010_01.json \
          -w $Y2010_01_mongodb_docs \
          -s 2010-01-01 \
          -e 2010-01-31 &

Y2010_02_mongodb_docs=$HOME/mongodb_documents/2010_02
touch $Y2010_02_mongodb_docs/parsed_info_2010_02.json
mkdir -p $Y2010_02_mongodb_docs
./main.py -t $TOKEN \
          -l $LOGIN \
          -d $Y2010_02_mongodb_docs \
          -i $Y2010_02_mongodb_docs/parsed_info_2010_02.json \
          -w $Y2010_02_mongodb_docs \
          -s 2010-02-01 \
          -e 2010-02-28 &


Y2010_03_mongodb_docs=$HOME/mongodb_documents/2010_03
touch $Y2010_03_mongodb_docs/parsed_info_2010_03.json
mkdir -p $Y2010_03_mongodb_docs
./main.py -t $TOKEN \
          -l $LOGIN \
          -d $Y2010_03_mongodb_docs \
          -i $Y2010_03_mongodb_docs/parsed_info_2010_03.json \
          -w $Y2010_03_mongodb_docs \
          -s 2010-03-01 \
          -e 2010-03-31 &
