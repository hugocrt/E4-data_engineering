from .elasticsearch_setup import es
from elasticsearch.helpers import bulk


def generate_data(documents):
    for document in documents:
        yield {
            "_index": "movies",
            "_source": {k: v if v else None for k, v in document .items()},
        }
