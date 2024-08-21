from elasticsearch import Elasticsearch, exceptions
from mage_ai.data_preparation.decorators import data_exporter

@data_loader
def test_retrieval(*args, **kwargs):
    index_name = kwargs.get('index_name', 'documents_20240821_*')
    query = kwargs.get('query', 'When is the next cohort?')
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    
    es_client = Elasticsearch([connection_string])
    
    search_query = {
        "size": 1,
        "query": {
            "match": {
                "text": query
            }
        }
    }
    
    try:
        response = es_client.search(
            index=index_name,
            body=search_query
        )
        
        if response['hits']['hits']:
            top_result = response['hits']['hits'][0]
            return top_result['_id']
        else:
            return "No results found."
    
    except exceptions.NotFoundError as e:
        return f"IndexNotFoundError: {e.info}"
    except exceptions.RequestError as e:
        return f"RequestError: {e.info}"
    except exceptions.TransportError as e:
        return f"TransportError: {e.info}"
    except Exception as e:
        return f"Unexpected error: {e}"
