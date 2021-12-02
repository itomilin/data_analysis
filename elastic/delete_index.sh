#!/bin/bash

curl -XDELETE \
     -H "Content-Type: application/json" \
     localhost:9200/big_data

