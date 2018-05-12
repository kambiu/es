from elasticsearch import Elasticsearch
import argparse

""" configuration """

indices_templates = {
    # index #1
    "student": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks" : {
                "read_only_allow_delete" : False
            }
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
            "number_of_replicas": 1,
            "blocks" : {
                "read_only_allow_delete" : False
            }
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
            "number_of_replicas" : 1,
            "blocks" : {
                "read_only_allow_delete" : False
            },
            "analysis": {
                "analyzer": {
                    # "my_stop_analyzer": { # only for stop wod
                    #     "type": "stop",
                    #     "stopwords_path": r"stopwords.txt",
                    #     #"stopwords": ["the", "a"]
                    # },
                    # "synonym" : { # only for synonym
                    #     "tokenizer" : "whitespace",
                    #     "filter" : ["my_synonym"]
                    # },
                    "my_custom_analyzer":{ # to integrate syonoym, stop word into one analyzer for the field
                        "type":      "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "my_synonym",
                            "my_stop",
                            "my_stemmer"
                        ]
                    }
                },
                "filter" : {
                    "my_synonym" : {
                        "type" : "synonym",
                        "synonyms_path" : r"synonym.txt"
                    },
                    "my_stop": {
                        "type":       "stop",
                        "stopwords_path": r"stopwords.txt",
                    },
                    "my_stemmer" : {
                        "type" : "stemmer",
                        "name" : "english"
                    }
                }
            }
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
                "content": {
                    "type": "text",
                    #"analyzer": "my_stop_analyzer" #Important define analyzer in setting here
                    "analyzer": "my_custom_analyzer"

                },
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
    },
    # index #5
    "chinese": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "blocks" : {
                "read_only_allow_delete" : False
            },
            "analysis": {
                "analyzer": {
                    "my_chinese_custom_analyzer":{ # to integrate syonoym, stop word into one analyzer for the field
                        "type":      "custom",
                        "tokenizer": "standard",
                        "filter": [ 
                            "my_synonym", # test whether chinese synonym and stop word can be applied
                            "my_stop",
                            "han_bigrams_filter"
                        ]
                    }
                },
                 "filter" : {
                    "my_synonym" : {
                        "type" : "synonym",
                        "synonyms_path" : r"synonym.txt"
                    },
                    "my_stop": {
                        "type":       "stop",
                        "stopwords_path": r"stopwords.txt",
                    },
                    "han_bigrams_filter" : {
                        "type" : "cjk_bigram",
                        "ignored_scripts": [
                            "hiragana",
                            "katakana",
                            "hangul"
                        ],
                        "output_unigrams" : True
                    }
                }
            }
        },
        "chinese": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "my_chinese_custom_analyzer"
                },
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


def main(es_index_name):
    es = Elasticsearch(["127.0.0.1:9200"])

    if es_index_name == "all":
        for index_name, config in indices_templates.items():
            create_index_mapping(es, index_name, config)
    else:
        create_index_mapping(es, es_index_name, indices_templates[es_index_name])



if __name__ == "__main__":

    help_ss = "You can choose one of the following indices to create: all|{}".format("|".join(indices_templates.keys()))
    parser = argparse.ArgumentParser()
    parser.add_argument("index", help=help_ss, type=str)
    args = parser.parse_args()

    main(args.index)
    print("Program end")