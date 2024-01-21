from .elasticsearch_setup import es_client
from elasticsearch.helpers import bulk


def generate_data(documents):
    for document in documents:
        yield {
            "_index": "movies",
            "_types": "movie",
            "_source": {k: v if v else None for k, v in document.items()},
        }


def count_per_field(field):
    mapping = es_client.indices.get_mapping(index='movies')
    field_type = mapping['movies']['mappings']['properties'].get(field, {}).get('type', None)
    if field_type == 'text':
        field_to_search = f"{field}.keyword"
    else:
        field_to_search = field

    query = {
        "size": 0,  # Utilisez 0 pour ne pas récupérer de documents, seulement les agrégations
        "aggs": {
            "counts": {
                "terms": {
                    "field": field_to_search,
                    "size": 10000
                }
            }
        }
    }
    result = es_client.search(index='movies', body=query)
    buckets = result['aggregations']['counts'].get('buckets', [])
    field_count_dict = {bucket['key']: bucket['doc_count'] for bucket in buckets}

    return field_count_dict


def search_movies(index_name, filters, page, page_size, order):

    body_query = {
        "bool": {
            "must": {"wildcard": {"title": {"value": f"*{filters.title}*"}}},
            "filter": []
        }
    }

    filters_fields = [f for f in dir(filters) if not f.startswith('__') and f != 'title']
    for field in filters_fields:
        filter_value = getattr(filters, field)
        if field.startswith("min_") or field.startswith("max_"):
            if filter_value != '':
                body_query['bool']['filter'].append(
                    {"range":
                        {field[4:]: {"gte" if field.startswith("min_") else "lte": filter_value}}
                     }
                )
        elif filter_value is not None and any(item.strip() for item in filter_value):
            body_query['bool']['filter'].append({"terms": {field+".keyword": filter_value}})

    from_value = (page - 1) * page_size

    result = es_client.search(
        index=index_name,
        body={
            "query": body_query,
            "from": from_value,
            "sort": [{"ranking": {"order": order}}],
            "size": page_size,
        }
    )

    hits = result['hits']['hits']
    total_hits = result['hits']['total']['value']
    info = (f"{total_hits} film{'s' if total_hits > 1 else ''} "
            f"correspondant à votre recherche (~{result['took']}ms)")
    return hits, total_hits, info


def create_index(es, documents):
    index_name = "movies"

    template_body = {
        "mappings": {
            "properties": {
                "ranking": {
                    "type": "integer"
                },
                "duration": {
                    "type": "integer"
                },
                "publication_year": {
                    "type": "integer"
                }
            }
        }
    }

    try:
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)

        else:
            es.indices.create(index=index_name, body=template_body)

        bulk(es, generate_data(documents))
        es.indices.refresh(index=index_name)

    except Exception as e:
        print(f"Error during index creation or bulk indexing: {e}")
