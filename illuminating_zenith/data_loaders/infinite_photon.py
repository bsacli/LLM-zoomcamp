from typing import Dict, List
from elasticsearch import Elasticsearch, exceptions

@data_loader
def search(*args, **kwargs) -> List[Dict[str, str]]:
    """
    Searches for documents in Elasticsearch based on a query.
    """
    
    # Default values
    connection_string = kwargs.get('connection_string', 'http://elasticsearch:9200')
    index_name = kwargs.get('index_name', 'documents_20240821_1906')  # Ensure index_name has a default value
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'text')
    
    # Get the query from args or use a default value
    query = args[0] if args else "When is the next cohort?"

    es_client = Elasticsearch(connection_string)
    
    # Construct the search query
    search_query = {
        "size": top_k,
        "query": {
            "match": {
                chunk_column: query  # Use chunk_column for flexibility
            }
        }
    }
    
    print("Sending search query:", search_query)
    try:
        response = es_client.search(
            index=index_name,
            body=search_query,
            _source=[chunk_column]
        )
        
        hits = response['hits']['hits']
        print("Search results:", hits)
        
        return hits
    
    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return []
    except exceptions.ConnectionError as e:
        print(f"ConnectionError: {e}")
        return []
    except exceptions.RequestError as e:
        print(f"RequestError: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Example usage
results = search("When is the next cohort?", index_name='documents_20240821_1906')
if results:
    top_result = results[0]
    print(f"Top matching result ID: {top_result['_id']}")
else:
    print("No results found.")
