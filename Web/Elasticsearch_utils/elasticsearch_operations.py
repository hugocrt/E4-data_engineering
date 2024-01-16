from .elasticsearch_setup import es
from elasticsearch.helpers import bulk


template_name = "ranking_template"
template_path = "static/ranking_template.json"


def generate_data(documents):
    for document in documents:
        yield {
            "_index": "movies",
            "_types": "movie",
            "_source": {k: v if v else None for k, v in document.items()},
        }


def search_movies(index_name, title_query, page_size, page=1, sort_order=None, min_year=None,
                  max_year=None):

    body_query = {"wildcard": {"title": {"value": f"*{title_query}*"}}}

    from_value = (page - 1) * page_size

    range_filter = [{"range": {"publication_year": {"gte": min_year}}},
                    {"range": {"publication_year": {"lte": max_year}}}]

    body_query = {"bool": {"must": body_query, "filter": range_filter}}

    result = es.search(
        index=index_name,
        body={
            "query": body_query,
            "from": from_value,
            "sort": [{"ranking": {"order": sort_order}}],
            "size": page_size,
        }
    )

    hits = result['hits']['hits']
    total_hits = result['hits']['total']['value']
    info = (f"{total_hits} film{'s' if total_hits > 1 else ''} correspondant à votre recherche (~{result['took']}ms)")
    return hits, total_hits, info


def clear_es_client(es_client=es, index='movies'):
    delete_query = {
        "query": {
            "match_all": {}
        }
    }
    response = es_client.delete_by_query(index=index, body=delete_query)
    es_client.indices.refresh(index=index)
    print(response)


def create_index(es_client, documents):
    index_name = "movies"

    template_body = {
        "mappings": {
            "properties": {
                "ranking": {
                    "type": "integer"
                }
            }
        }
    }

    try:
        if not es.indices.exists(index=index_name):
            es_client.indices.create(index=index_name, body=template_body)

        response = bulk(es_client, generate_data(documents))
        print(response)

        es_client.indices.refresh(index=index_name)

    except Exception as e:
        print(f"Error during index creation or bulk indexing: {e}")
