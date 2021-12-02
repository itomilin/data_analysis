#!/bin/bash

read -rd '' mapping << EOF
{
  "mappings": {
    "properties": {
      "all_lines": {
        "type": "long"
      },
      "another_files": {
        "type": "long"
      },
      "another_languages": {
        "properties": {
          "count": {
            "type": "long"
          },
          "name": {
            "type": "keyword"
          }
        }
      },
      "branches": {
        "type": "keyword"
      },
      "build_system": {
        "properties": {
          "cmake": {
            "type": "boolean"
          },
          "make": {
            "type": "boolean"
          },
          "meson": {
            "type": "boolean"
          },
          "ms_build": {
            "type": "boolean"
          },
          "qmake": {
            "type": "boolean"
          }
        }
      },
      "contributors_female": {
        "type": "long"
      },
      "contributors_male": {
        "type": "long"
      },
      "contributors_total_count": {
        "type": "long"
      },
      "contributors_unrecognized": {
        "type": "long"
      },
      "count_spaces": {
        "type": "long"
      },
      "count_tabs": {
        "type": "long"
      },
      "cpp_src_files": {
        "type": "long"
      },
      "cpp_src_lines": {
        "type": "long"
      },
      "created_at": {
        "type": "date"
      },
      "description": {
        "type": "keyword"
      },
      "dockerfile": {
        "type": "boolean"
      },
      "forks": {
        "type": "long"
      },
      "full_name": {
        "type": "text"
      },
      "indention_method": {
        "type": "keyword"
      },
      "indention_method_dominate": {
        "type": "text"
      },
      "issue_titles": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "issues_close": {
        "type": "long"
      },
      "issues_open": {
        "type": "long"
      },
      "license": {
        "type": "keyword"
      },
      "readme": {
        "type": "boolean"
      },
      "stars": {
        "type": "long"
      },
      "total_issues": {
        "type": "long"
      },
      "updated_at": {
        "type": "date"
      }
    }
  }
}
EOF

curl -XPUT \
     -H "Content-Type: application/json" \
     http://localhost:9200/big_data \
     -d "${mapping}"

