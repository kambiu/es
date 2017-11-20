from elasticsearch import Elasticsearch


es = Elasticsearch(["127.0.0.1:9200"])


""" configuration """

indices_templates = {
    # index #1
    "school": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        # same field name in same index but different type cannot have different analyzer, eg. date_modified
        # aka in one index, one field name only one mapping can be applied
        "type_mappings": {
            # type 1 of index #1
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
            },
            # type 2 of index #1
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
        }
    },
    # index #2
    "backery": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas" : 1
        },
        "type_mappings": {
            # type 1 of index #2
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
        }
    },
    # index #3
    "words": {
        "index_settings": {
            "number_of_shards": 1,
            "number_of_replicas" : 1
        },
        "type_mappings": {
            # type 1 of index #2
            "autocomplete": {
                "properties": {
                    "suggest": {"type": "completion"}
                }
            }
        }
    }
}

""" end configuration """


def create_index_mapping():
    for index_name, config in indices_templates.items():
        # create index with shards & replica
        es.indices.delete(index=index_name, ignore=([404]))
        es.indices.create(index=index_name, body=config["index_settings"])

        # create mapping for each types in the index creating
        for type, prop in config["type_mappings"].items():
            print("{} {}".format(type, prop))
            es.indices.put_mapping(index=index_name, doc_type=type, body=prop)


def main():
    create_index_mapping()
    print("Program end")


if __name__ == "__main__":
    # main()
    main()