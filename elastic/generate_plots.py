#!/usr/bin/python3.9

################################################################################
#######################PLEASE DON`T SCROLL DOWN#################################
#######################PLEASE DON`T SCROLL DOWN#################################
#######################PLEASE DON`T SCROLL DOWN#################################
#######################PLEASE DON`T SCROLL DOWN#################################
################################################################################

import requests
import json
import matplotlib.pyplot as plt

URL_SEARCH = 'http://localhost:9200/big_data/_search'
URL_COUNT = "http://localhost:9200/big_data/_count"
HEADERS = {'Content-type': 'application/json',
           'Accept-Charset': 'UTF-8'}

LICENCE_QUERY = """
{
    "size": 0,
    "aggs": {
    "agg_query": {
        "terms": {
            "field": "license",
            "size": 100
        }
    }
  }
}
"""

DOCKERFILE_QUERY = """
{
  "size": 0,
  "aggs": {
    "agg_query": {
      "terms": {
          "field": "dockerfile",
          "size": 2
      }
    }
  }
}
"""

README_QUERY = """
{
  "size": 0,
  "aggs": {
    "agg_query": {
      "terms": {
          "field": "readme",
          "size": 2
      }
    }
  }
}
"""

CONTRIBUTORS_QUERY = """
{
  "size": 0,
  "aggs": {
    "female": {
      "sum": { "field": "contributors_female" }
    },
    "male": {
      "sum": { "field": "contributors_male" }
    },
    "unrecognized": {
      "sum": { "field": "contributors_unrecognized" }
    }
  }
}
"""

BUILD_SYSTEM_QUERY = """
{
  "size": 0,
  "aggs": {
    "meson": {
      "sum": { "field": "build_system.meson" }
    },
    "cmake": {
      "sum": { "field": "build_system.cmake" }
    },
    "qmake": {
      "sum": { "field": "build_system.qmake" }
    },
    "make": {
      "sum": { "field": "build_system.make" }
    },
    "ms_build": {
      "sum": { "field": "build_system.ms_build" }
    }
  }
}
"""

INDENTATION_METHOD_QUERY = """
{
    "size": 0,
    "aggs": {
    "agg_query": {
        "terms": {
            "field": "indention_method",
            "size": 3
        }
    }
  }
}
"""

# BRANCHES ##
GITFLOW_R_D_M_QUERY = """
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "branches": "master"
          }
        },
        {
          "term": {
            "branches": "release"
          }
        },
        {
          "term": {
            "branches": "develop"
          }
        }
      ]
    }
  }
}
"""

GITFLOW_D_M_QUERY = """
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "branches": "master"
          }
        },
        {
          "term": {
            "branches": "develop"
          }
        }
      ]
    }
  }
}
"""

BRANCHES_QUERY = """
{
  "size": 0,
  "aggs": {
    "agg_query": {
      "terms": {
          "field": "branches",
          "size": 10
      }
    }
  }
}
"""
############

NO_BUILD_SYSTEM_QUERY = """
{
  "from": 0, 
  "aggs": {
    "keys": {
      "composite": {
        "sources": [
          {
            "build_system.meson": {
              "terms": {
                "field": "build_system.meson"
              }
            }
          },
          {
            "build_system.cmake": {
              "terms": {
                "field": "build_system.cmake"
              }
            }
          },
          {
            "build_system.qmake": {
              "terms": {
                "field": "build_system.qmake"
              }
            }
          },
          {
            "build_system.make": {
              "terms": {
                "field": "build_system.make"
              }
            }
          },
          {
            "build_system.ms_build": {
              "terms": {
                "field": "build_system.ms_build"
              }
            }
          }
        ], 
        "size": 5
      }
    }
  }, 
  "size": 0
}
"""

ANOTHER_LANGUAGES_QUERY = """
{
  "size": 0,
  "aggs": {
    "agg_query": {
      "terms": {
          "field": "another_languages.name",
          "size": 20
      }
    }
  }
}
"""

SOURCE_CODE_QUERY = """
{
  "size": 10,
  "sort": [
    {
      "cpp_src_lines": {
        "order": "desc"
      }
    }
  ]
}
"""

DESCRIPTION_QUERY = """
{
  "size": 0,
  "aggs": {
    "agg_query": {
      "terms": {
          "field": "description",
          "size": 1
      }
    }
  }
}
"""

IDEAL_QUERY = """
{
  "size": 30,
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "branches": "master"
          }
        },
        {
          "term": {
            "branches": "develop"
          }
        },
        {
          "term": {
            "readme": true
          }
        },
        {
          "term": {
            "build_system.make": true
          }
        },
        {
          "term": {
            "indention_method": "space"
          }
        }
      ],
      "must_not": [
       {
        "term": {
          "license": "NO_DATA"
        }
       },
       {
        "term": {
          "description": "NO_DATA"
        }
       }
      ]
    }
  }
}
"""

STARS_QUERY = """
{
  "size": 10,
  "sort": [
    {
      "stars": {
        "order": "desc"
      }
    }
  ]
}
"""


def auto_label_bar_h(rects, ax):
    for rect in rects:
        width = rect.get_width()
        # shift, ..., value,
        ax.text(width, rect.get_y() + rect.get_height() / 2.0,
                '%d' % int(width), ha='left', va='center')


def auto_label_bar(rects, ax):
    data_sum = rects.datavalues.sum()

    for rect in rects:
        height = rect.get_height()
        percent = int(height) / data_sum * 100
        ax.text(x=rect.get_x() + rect.get_width() / 2.0, y=height,
                s="{:.2f}%".format(percent), va='center')


def license_analyse():
    picture_name = "license.png"

    response = requests.post(url=URL_SEARCH, data=LICENCE_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    buckets = json_response['aggregations']['agg_query']['buckets']
    license_names = []
    count = []
    for bucket in buckets:
        license_names.append(bucket['key'])
        count.append(bucket['doc_count'])

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 9)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=9, bottom=True,
                   left=True)

    bars = plt.barh(license_names, count)
    ax.yaxis.set_label_position('right')
    for tick in ax.get_yticklabels():
        tick.set_rotation(50)
    auto_label_bar_h(bars, ax)
    ax.set_title('Популярность найденных лицензий в репозиториях')
    ax.set_xlabel('Количество найденных лицензий')
    ax.set_ylabel("Название лицензии")

    fig.savefig(f'./plots/{picture_name}')


def dockerfile_analyse():
    picture_name = "dockerfiles.png"

    response = requests.post(url=URL_SEARCH, data=DOCKERFILE_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    buckets = json_response['aggregations']['agg_query']['buckets']
    values = []
    labels = []
    for bucket in buckets:
        if bucket['key_as_string'] == "false":
            values.append(bucket['doc_count'])
            labels.append(bucket['key_as_string'])
        elif bucket['key_as_string'] == "true":
            values.append(bucket['doc_count'])
            labels.append(bucket['key_as_string'])

    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6.5)
    ax.pie(values, labels=labels, autopct='%.2f%%')
    ax.set_title('Наличие Dockerfile\nманифеста в репозиториях')

    fig.savefig(f'./plots/{picture_name}')


def readme_analyse():
    picture_name = "readme.png"

    response = requests.post(url=URL_SEARCH, data=README_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    buckets = json_response['aggregations']['agg_query']['buckets']
    values = []
    labels = []
    for bucket in buckets:
        if bucket['key_as_string'] == "false":
            values.append(bucket['doc_count'])
            labels.append(bucket['key_as_string'])
        elif bucket['key_as_string'] == "true":
            values.append(bucket['doc_count'])
            labels.append(bucket['key_as_string'])

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    ax.pie(values, labels=labels, autopct='%.6f%%')
    ax.set_title('Наличие README\nв репозиториях')

    fig.savefig(f'./plots/{picture_name}')


def contributors_analyse():
    picture_name = "contributors.png"

    response = requests.post(url=URL_SEARCH, data=CONTRIBUTORS_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)

    values = []
    labels = []

    female = json_response['aggregations']['female']['value']
    male = json_response['aggregations']['male']['value']
    unrecognized = json_response['aggregations']['unrecognized'][
        'value']
    values.append(female)
    values.append(male)
    values.append(unrecognized)
    labels.append("female")
    labels.append("male")
    labels.append("unrecognized")

    fig, ax = plt.subplots()
    fig.set_size_inches(9, 9)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.tick_params(axis='x', which='both', labelsize=15, bottom=True,
                   left=False)
    ax.pie(values, labels=labels, autopct='%.2f%%')
    ax.set_title('Процентное отношение распознанного пола\nпо аватару разработчиков')

    fig.savefig(f'./plots/{picture_name}')


def build_system_analyse():
    picture_name = "build_system.png"

    response = requests.post(url=URL_SEARCH, data=BUILD_SYSTEM_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)

    ms_build = json_response['aggregations']['ms_build']['value']
    qmake = json_response['aggregations']['qmake']['value']
    cmake = json_response['aggregations']['cmake']['value']
    meson = json_response['aggregations']['meson']['value']
    make = json_response['aggregations']['make']['value']

    values = [ms_build, qmake, cmake, meson, make]
    labels = ["ms_build", "qmake", "cmake", "meson", "make"]

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.tick_params(axis='x', which='both', labelsize=15, bottom=True,
                   left=False)
    bars = plt.bar(labels, values)
    auto_label_bar(bars, ax)

    ax.set_title('Процентное отношение\nанализируемых систем сборки')
    ax.set_xlabel('Название систем сборки')
    ax.set_ylabel('Количество')

    fig.savefig(f'./plots/{picture_name}')


def no_build_system_analyse():
    picture_name = "repo_without_build_system.png"

    response = requests.post(url=URL_SEARCH, data=NO_BUILD_SYSTEM_QUERY,
                             headers=HEADERS)
    total_count = requests.get(url=URL_COUNT, headers=HEADERS)
    json_response_count = json.loads(total_count.text)['count']
    json_response = json.loads(response.text)

    count_no_builds = 0
    no_builds = json_response['aggregations']['keys']['buckets']
    for build in no_builds:
        meson = build['key']['build_system.meson']
        cmake = build['key']['build_system.cmake']
        qmake = build['key']['build_system.qmake']
        make = build['key']['build_system.make']
        ms_build = build['key']['build_system.ms_build']
        if not any([meson, cmake, qmake, make, ms_build]):
            count_no_builds = build['doc_count']
            break

    values = [count_no_builds, json_response_count]
    labels = ["without_builds", "total"]

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 7)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=15, bottom=True,
                   left=False)
    ax.pie(values, labels=labels, autopct='%.2f%%')
    ax.set_title('Отношение репозиториев \nс системой сборки и без')

    fig.savefig(f'./plots/{picture_name}')


def top_ten_branches_analyse():
    picture_name = "top_10_github_branches.png"

    response = requests.post(url=URL_SEARCH, data=BRANCHES_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)

    values = []
    labels = []
    branches = json_response['aggregations']['agg_query']['buckets']
    for build in branches:
        values.append(build['doc_count'])
        labels.append(build['key'])

    fig, ax = plt.subplots()
    fig.set_size_inches(15.7, 11.27)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=15, bottom=True,
                   left=False)
    bars = plt.barh(labels, values)
    auto_label_bar_h(bars, ax)
    ax.yaxis.set_label_position('right')
    ax.set_title('Топ 10 самых популярных названий веток')
    ax.set_xlabel('Количество')
    ax.set_ylabel('Название веток')

    fig.savefig(f'./plots/{picture_name}')


def gitflow_analyse():
    picture_name = "gitflow.png"

    response = requests.post(url=URL_SEARCH, data=GITFLOW_R_D_M_QUERY,
                             headers=HEADERS)
    json_response_rdm = json.loads(response.text)
    response = requests.post(url=URL_SEARCH, data=GITFLOW_D_M_QUERY,
                             headers=HEADERS)
    json_response_dm = json.loads(response.text)

    values = [json_response_rdm['hits']['total']['value'],
              json_response_dm['hits']['total']['value']]
    labels = ["release-master-develop", "master-develop"]

    fig, ax = plt.subplots()
    fig.set_size_inches(8.7, 8.27)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=12, bottom=True,
                   left=False)

    bars = plt.bar(labels, values)
    for rect in bars:
        height = rect.get_height()
        percent = int(height)
        ax.text(x=rect.get_x() + rect.get_width() / 2.0, y=height,
                s="{:}".format(percent), va='center')
    ax.set_title('Репозитории с моделью ведения - Git Flow')
    ax.set_xlabel('Комбинация веток')
    ax.set_ylabel('Количество')

    fig.savefig(f'./plots/{picture_name}')


def another_languages_analyse():
    picture_name = "another_languages.png"

    response = requests.post(url=URL_SEARCH, data=ANOTHER_LANGUAGES_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    values = []
    labels = []

    for item in json_response['aggregations']['agg_query']['buckets']:
        labels.append(item['key'])
        values.append(item['doc_count'])

    fig, ax = plt.subplots(figsize=(6,4), dpi=100)
    fig.set_size_inches(11.7, 8.27)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=12, bottom=True,
                   left=False)

    bars = plt.barh(labels, values)
    auto_label_bar_h(bars, ax)
    ax.yaxis.set_label_position('right')
    ax.set_title('Наиболее часто встречающиеся языки\n совместно с C++')
    ax.set_xlabel('Количество')
    ax.set_ylabel('Языки')

    fig.savefig(f'./plots/{picture_name}')


def cpp_source_analyse():
    picture_name = "cpp_source_top_10.png"

    response = requests.post(url=URL_SEARCH, data=SOURCE_CODE_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    values = []
    labels = []

    for item in json_response['hits']['hits']:
        labels.append(item['_source']['full_name'])
        values.append(item['_source']['cpp_src_lines'])

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=10, bottom=True,
                   left=False)
    for tick in ax.get_yticklabels():
        tick.set_rotation(50)
    ax.set_xlabel('Количество строк')
    ax.set_ylabel('Имя репозитория')
    # ax.set_xlim(0, 45000)

    fig.set_size_inches(16.7, 8.27)

    bars = plt.barh(labels, values)
    auto_label_bar_h(bars, ax)
    ax.yaxis.set_label_position('right')
    ax.set_title('Топ 10 репозиториев по количеству строк исходного кода')

    fig.savefig(f'./plots/{picture_name}')


def indention_method_analyse():
    picture_name = "indention_method.png"

    response = requests.post(url=URL_SEARCH,
                             data=INDENTATION_METHOD_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    values = []
    labels = []

    for item in json_response['aggregations']['agg_query']['buckets']:
        labels.append(item['key'])
        values.append(item['doc_count'])

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%.2f%%')

    ax.tick_params(axis='both', which='both', labelsize=9, bottom=True,
                   left=False)
    ax.set_title('Типы отступов')

    fig.savefig(f'./plots/{picture_name}')


def description_analyse():
    picture_name = "description.png"

    response = requests.post(url=URL_SEARCH,
                             data=DESCRIPTION_QUERY,
                             headers=HEADERS)
    total_count = requests.get(url=URL_COUNT, headers=HEADERS)
    json_response_count = json.loads(total_count.text)['count']
    json_response = json.loads(response.text)
    no_builds = json_response['aggregations']['agg_query']['buckets']
    count_no_builds = no_builds[0]['doc_count']
    label = no_builds[0]['key']

    values = [count_no_builds, json_response_count]
    labels = [label, "WITH_DATA"]

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 7)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=15, bottom=True,
                   left=False)
    ax.pie(values, labels=labels, autopct='%.2f%%')
    ax.set_title('Отношение репозиториев \nс наличием описания и без')

    fig.savefig(f'./plots/{picture_name}')


def ideal_analysis():
    picture_name = "ideal.png"

    response = requests.post(url=URL_SEARCH,
                             data=IDEAL_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    values = []
    labels = []
    total = json_response['hits']['total']['value']
    for item in json_response['hits']['hits']:
        labels.append(item['_source']['full_name'])
        values.append(item['_source']['stars'])

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    fig.set_size_inches(18.7, 8.27)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=10, bottom=True,
                   left=True)

    bars = plt.barh(labels, values)
    auto_label_bar_h(bars, ax)
    ax.yaxis.set_label_position('right')
    ax.set_title(f'Репозитории с качественным стилем ведения,\n всего {total}')
    ax.set_ylabel('Наименование')
    ax.set_xlabel('Количество звезд')

    fig.savefig(f'./plots/{picture_name}')


def stars_analysis():
    picture_name = "stars.png"

    response = requests.post(url=URL_SEARCH,
                             data=STARS_QUERY,
                             headers=HEADERS)
    json_response = json.loads(response.text)
    values = []
    labels = []
    for item in json_response['hits']['hits']:
        labels.append(item['_source']['full_name'])
        values.append(item['_source']['stars'])

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    fig.set_size_inches(18.7, 8.27)
    plt.rcParams['axes.edgecolor'] = '#333F4B'
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', labelsize=10, bottom=True,
                   left=True)

    bars = plt.barh(labels, values)
    auto_label_bar_h(bars, ax)
    ax.yaxis.set_label_position('right')
    ax.set_title(f'Наиболее популярные репозитории по звездам')
    ax.set_ylabel('Наименование')
    ax.set_xlabel('Количество звезд')

    fig.savefig(f'./plots/{picture_name}')


if __name__ == '__main__':
    plt.rc('font', size=16)  # controls default text size
    plt.rc('axes', titlesize=26)  # fontsize of the title
    plt.rc('axes', labelsize=26)  # fontsize of the x and y labels
    plt.rc('legend', fontsize=16)  # fontsize of the legend
    try:
        dockerfile_analyse()
        license_analyse()
        readme_analyse()
        contributors_analyse()
        build_system_analyse()
        no_build_system_analyse()
        top_ten_branches_analyse()
        gitflow_analyse()
        another_languages_analyse()
        cpp_source_analyse()
        indention_method_analyse()
        description_analyse()
        ideal_analysis()
        stars_analysis()
    except requests.exceptions.ConnectionError:
        print("[ ERROR ] Failed to establish a new connection.")
        exit(1)
