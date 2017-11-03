import argparse
import elasticsearch


def index_from_file(file, host, port):
    es = elasticsearch.Elasticsearch(['{}:{}'.format(host, port)])

    with open(file, "r", encoding="utf-8") as f:
        str_json = f.read()
        r = es.bulk(body=str_json)
        print(r)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File path of json data to be indexed")
    parser.add_argument("es_host", nargs='?', help="elatsicsearch host")
    parser.add_argument("es_port", nargs='?', help="elatsicsearch port")
    args = parser.parse_args()

    if args.es_host is None:
        args.es_host = "localhost"

    if args.es_port is None:
        args.es_port = 9200

    index_from_file(args.file, args.es_host, args.es_port)
    print("\n==============\nProgram end\n==============")