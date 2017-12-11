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
        results = es.search(index="student", doc_type="student", body=json.dumps(query_dsl))
        print("Number of returns [pagination-start from {}]: {}".format(start, len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)


def boolean_query(es):
    """
    must: all condition inside must fulfill and with score calculated
    filter: all condition inside must fulfill and without score calculated
    should: anyone if conditions fulfill
    must_not: all condition inside must NOT NOT NOT fulfill
    """
    bool_choice = ["must", "filter", "should", "must_not"]
    for choice in bool_choice:
        query_dsl = {
            "from": 0,
            "size": 1000,
            "_source": ["grade", "age"],
            "query": {
                "bool":{
                    # either a single dict or a list of dict
                    choice: [
                        {"range": {
                            "age": {
                                "gte": 15,
                                "lte": 18
                            }
                        }},
                        { "term": {"grade": "A"}}
                    ]
                }
            }
        }
        results = es.search(index="student", doc_type="student", body=json.dumps(query_dsl))
        # print(results)
        print("Number of returns [boolean_query-{}]: {}".format(bool_choice, len(results["hits"]["hits"])))



def field_text(es):
    """
    # term must be a keyword
    MATCH = term: { field_name, value}
        = terms :{fieldname, [value1, value2 ...]} match any one of the value
    STRING = wildcard query or regular express
    EXISTS = exists
    EMPTY = exists + must_not
    LESS = range
    GREATER = range
    """
    field_text_options = [
        # terms must be keyword in mapping
        {"term": {"grade": "F"}}, # match
        {"terms": {"grade": ["C", "D"]}},  # matchover ~ match any one of the value
        {"exists": {"field": "grade"}},  # empty is must_not + exists - not need to be keyword
        {"range": {"age": {
            "gt": 12,
            "lte": 14
        }}},  # empty is must_not + exists
        {"prefix": {"courses": "Hi"}},  # also must to be keyword field
        {"regexp": {"courses": ".*great.*"}},  # allow non keyword
        {"wildcard": {"courses": "great*"}}  # allow non keyword
    ]


    for option in field_text_options:
        query_dsl = {
            "from": 0,
            "size": 1000,
            "_source": ["grade", "age", "courses"],
            "query": option
        }
        results = es.search(index="student", doc_type="student", body=json.dumps(query_dsl))
        # print(results)
        print("Number of returns [field_text={}]: {}".format(list(option.keys())[0], len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)


def stemming(es):
    words = ["start", "starts"]
    for word in words:
        query_dsl = {
            "_source": "*",
            "query": {
                "match": {"content": word}
            },
            "highlight": {
                "fields": {
                    "content": {}
                }
            }
        }
        results = es.search(index="student", doc_type="student", body=json.dumps(query_dsl))
        print("Number of returns [stemming-{}]: {}".format(word, len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node["highlight"])


def sorting(es):

    name = ["date_created asc > score", "score > date_modified desc", "height desc", "age asc"]

    # order is require for date fields ?
    options = [
        [{"date_created": {"order": "asc"}}, "_score"],
        ["_score", {"date_modified": {"order": "desc"}}],
        {"height":  "desc"},
        {"age": "asc"}
    ]

    for idx, option in enumerate(options):

        query_dsl = {
            "from": 0, "size": 100,
            "_source": ["_score", "age", "height", "date_created", "date_modified"],
            "query": {
                "match": {"content": "change"}
            },
            "highlight": {
                "fields": {
                    "content": {}
                }
            },
            "sort": option
        }

        results = es.search(index="student", doc_type="staff", body=json.dumps(query_dsl), filter_path=['hits.hits.*'])
        print("Number of returns [sorting-{}]: {}".format(name[idx], len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)
    pass


def sorting_with_array(es):

    for sorting_method in ["avg", "min", "max", "sum", "median"]:
        query_dsl = {
            "from": 0, "size": 100,
            "_source": ["weight"],
            "query": {
                "match": {"content": "change"}
            },

            "sort": {"weight": {"order": "asc", "mode": sorting_method}}
        }

        results = es.search(index="cake", doc_type="cake", body=json.dumps(query_dsl))
        print("Number of returns [sorting_with_array-{}]: {}".format(sorting_method, len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)


def aggregation(es):

    query_dsl = {
        "from": 0,
        "size": 1000,
        "query": {
            "match_all": {}
            # "match": {"content": "test"}
        },
        "aggs": {
            # "grade_value_count": {  # number of distinct value in this field
            #     "value_count": {"field": "grade"}
            # },
            # "price_stats": { # include info of avg, max, min, sum
            #     "stats": {"field": "price" }
            # },

            # multiple level parametric
            "grade_term_agg": {
                # "terms": {"field": "grade", "order": {"_count": "asc"}}
                "terms": {"field": "grade", "order": {"_term": "asc"}},
                "aggs":{
                    "level2": {
                        "terms": {"field": "active"}
                    }
                }
            }

        }
    }

    # results = es.search(body=json.dumps(query_dsl))
    results = es.search(index="_all", doc_type=",", body=json.dumps(query_dsl))
    # print(results)
    print("Number of returns [aggregation-{}]: {}".format(1, len(results["hits"]["hits"])))
    for key, value in results["aggregations"].items():
        print(key, value)


def suggest(es):

    #TODO find out the context suggester later

    options = [
        {
            # phrase suggester is configured through index mapping
            "term_suggester": {
                "text": "sguar", # give a  wrong word and suggest back sugar
                "term": {"field": "content"}
            }
        },

        # completeion_suggester refer to autocomplete.html

        # }},{"suggest2":{
        #         "text": "sugar",
        #         "term": {"field": "content"}
        # }},{"suggest3":{
        #         "text": "sugar",
        #         "term": {"field": "content"}
        # }},{"suggest4":{
        #         "text": "sugar",
        #         "term": {"field": "content"}
        # }},{"suggest5":{
        #         "text": "sugar",
        #         "term": {"field": "content"}
        # }}
    ]

    for option in options:
        query_dsl = {
            "from": 0,
            "size": 1000,
            "query": {
                "match": {"content": "sugar"}
            },
            "suggest": option
        }

        # results = es.search(body=json.dumps(query_dsl))
        results = es.search(index="_all", doc_type="", body=json.dumps(query_dsl))
        # print(results)
        print("Number of returns [suggest-{}]: {}".format(list(option.keys())[0], len(results["hits"]["hits"])))

        for value in results["suggest"][list(option.keys())[0]]:
            print(value)


def score(es):
    """
    function to define score of query
    1. use function score --> redefine the score caluculation ??
    2. use boosting query --> adjust score based on terms
    """

    # 2 boosting query
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-boosting-query.html

    # must require both positive terms & negative terms
    # positive -->  normal query words
    # negative --> undesirable words
    # negative_boost --> lower the words proirity
    queries = {
        "normal_query": {
            "match": {"content": "get"}
        },
        "boost_query": {
            "boosting" : {
                "positive" : {
                    "match" : {
                        "content" : "get"
                    }
                },
                "negative" : {
                    "term" : {
                        "content" : "happy"
                    }
                },
                "negative_boost" : 0.2
            }
        }
    }

    for key, value in queries.items():
        print(key)
        query_dsl = {
            "from": 0, "size": 100,
            "_source": ["grade"],
            "query": { }
        }
        query_dsl["query"] = value

        print(query_dsl)

        results = es.search(index="cake", doc_type="cake", body=json.dumps(query_dsl))
        print("Number of returns [score-{}-query]: {}".format(key, len(results["hits"]["hits"])))
        for node in results["hits"]["hits"]:
            print(node)


def test_analyzers(es):
    """
    #TODO
    stemming
    stopwords
    filters
    https://www.elastic.co/guide/en/elasticsearch/reference/current/_testing_analyzers.html
    """
    all_tokenizers = {
        "1": {
            "analyzer": "whitespace",
            "text":     "The quick brown fox."
        },
        "2": {
            "tokenizer": "standard",
            "filter":  [ "lowercase", "asciifolding" ],
            "text":      "Is this déja vu?"
        }
    }
    es_idx = elasticsearch.client.IndicesClient(es)

    for key, value in all_tokenizers.items():
        results = es_idx.analyze(index=None, body=json.dumps(value))
        print("--- {}".format(key))
        print(results)


def main():
    host = "localhost"
    port = 9200
    es = elasticsearch.Elasticsearch(['{}:{}'.format(host, port)])
    test_analyzers(es)


if __name__ == "__main__":
    main()
