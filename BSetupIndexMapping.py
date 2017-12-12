from elasticsearch import Elasticsearch
import argparse

""" configuration """

indices_templates = {
    # index #1
    "student": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "student": {
            "properties": {
                "date_created": {
                    "type": "date",
                    "format": "epoch_millis"
                },
                "date_modified": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||dd/MM/yyyy HH:mm:ss"
                },
                "age": {"type": "integer"},
                "height": {"type": "float"},
                "courses": {"type": "keyword"},
                "grade": {"type": "keyword"},
                "content": {"type": "text"},
                "active": {"type": "boolean"}
            }
        }
    },
    "staff": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "staff": {
            "properties": {
                "date_created": {
                    "type": "date",
                    "format": "epoch_millis"
                },
                "date_modified": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||dd/MM/yyyy HH:mm:ss"
                },
                "age": {"type": "integer"},
                "height": {"type": "float"},
                "courses": {"type": "keyword"},
                "content": {"type": "text"},
                "active": {"type": "boolean"}
            }
        }
    },
    # index #2
    "cake": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas" : 1
        },
        "cake": {
            "properties": {
                "date_created": {
                    "type": "date",
                    "format": "epoch_millis"
                },
                "date_expired": {
                    "type": "date",
                    "format": "yyyy/MM/dd"
                },
                "price": {"type": "float"},
                "weight": {"type": "float"},
                "grade": {"type": "keyword"},
                "content": {"type": "text"},
                "active": {"type": "boolean"}
            }
        }
    },
    # index #3
    "words": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas" : 1
        },
        "words": {
            "properties": {
                "suggest": {"type": "completion"}
            }
        }
    }
}

""" end configuration """


def create_index_mapping(es, index_name, config):    
    # create index with shards & replica
    es.indices.delete(index=index_name, ignore=([404]))
    es.indices.create(index=index_name, body=config["index_settings"])
    es.indices.put_mapping(index=index_name, doc_type=index_name, body=config[index_name])


def setup_stopword(es, idx_name):
    """
    Stop word is following to specific index
    """
    analysis_settings = {
        "analysis": {
            "analyzer": {
                "my_english_analyzer": {
                    "type": "standard",
                    "max_token_length": 5,
                    "stopwords": "_english_"
                }
            }
        }
    }
    es.indices.close(idx_name)
    print("Putting settings...")
    es.indices.put_settings(index=idx_name, body=analysis_settings)
    es.indices.open(idx_name)


def main(es_index_name):
    es = Elasticsearch(["127.0.0.1:9200"])

    if es_index_name == "all":
        for index_name, config in indices_templates.items():
             create_index_mapping(es, index_name, config)
    else:
        create_index_mapping(es, es_index_name, indices_templates[es_index_name])

    if es_index_name == "cake":
        setup_stopword(es, "cake")


if __name__ == "__main__":

    help_ss = "You can choose one of the following indices to create: all|{}".format("|".join(indices_templates.keys()))
    parser = argparse.ArgumentParser()
    parser.add_argument("index", help=help_ss, type=str)
    args = parser.parse_args()

    main(args.index)
    print("Program end")