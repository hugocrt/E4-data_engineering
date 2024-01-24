from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

try:
    es_client = Elasticsearch(hosts=["http://elasticsearch:9200"])
    # Check the cluster health
    cluster_health = es_client.cluster.health()
    print(cluster_health)

except ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
