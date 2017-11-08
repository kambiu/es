import elasticsearch
import json

""" notes 

body is Query DSL in json format

"""


def query_all(es):

    dict_query_dsl ={
        "query": {
            "match_all": {}
        }
    }
    # return is already dict not json
    results = es.search(index="school", doc_type="student", body=json.dumps(dict_query_dsl))
    print("Number of returns [query_all]: {}".format(len(results["hits"]["hits"])))
    for node in results["hits"]["hits"]:
        print(node)


def print_fields(es):

    # choose what fields to print
    fields_to_display_csv = [
        ["date_*"],
        ["age", "height"],
        ["courses"]
    ]

    for fields_csv in fields_to_display_csv:
        query_dsl = {
            "_source": fields_csv,
            "query": {
                "match_all": {}
            }
        }
        results = es.search(index="school", doc_type="student", body=json.dumps(query_dsl))
        print("Number of returns [print_fields-]: {}".format(len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)


def highlight_and_summary(es):
    # choose what fields to highlight --> usualy from content or title
    query_dsl = {
        "_source": "*",
        "query": {
            "match": {"content": "with"}
        },
        "highlight": {
            "fields": {
                "content": {}
            }
        }
    }
    results = es.search(index="school", doc_type="student", body=json.dumps(query_dsl))
    print("Number of returns [print_fields-]: {}".format(len(results["hits"]["hits"])))
    for node in results["hits"]["hits"]:
        print(node["highlight"])


def pagination(es):
    # choose what fields to highlight --> usualy from content or title

    starts = [0, 9, 18]

    for start in starts:
        query_dsl = {
            "from": start, "size": 10,
            "_source": "",
            "query": {
                "match": {"content": "the"}
            }
        }
        results = es.search(index="school", doc_type="student", body=json.dumps(query_dsl))
        print("Number of returns [pagination-start from {}]: {}".format(start, len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)


def main():
    host = "localhost"
    port = 9200
    es = elasticsearch.Elasticsearch(['{}:{}'.format(host, port)])
    pagination(es)


if __name__ == "__main__":
    main()
