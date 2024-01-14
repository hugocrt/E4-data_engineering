from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

try:
    # Create a connection to Elasticsearch (assuming it's running on localhost:9200)
    es = Elasticsearch(hosts=["http://localhost:9200"])

    # Check the cluster health
    cluster_health = es.cluster.health()
    print(cluster_health)

except ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
