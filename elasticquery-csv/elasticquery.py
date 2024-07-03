import csv
from elasticsearch import Elasticsearch
import json
import traceback
import logging

with open('config.json', 'r') as f:
    configs = json.load(f)

output_csv_file = 'output_logs.csv'

# Loop through each configuration
for config in configs:
    # Initialize Elasticsearch client with extended timeout
    es = Elasticsearch(
        cloud_id=config["cloud_id"],
        api_key=config["api_key"],
        timeout=3000  # Extended timeout
    )

    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": config["start_date"],
                    "lte": config["end_date"]
                }
            }
        }
    }

    # Open CSV file and write data
    with open(output_csv_file, mode='w', newline='') as file:
        writer = None  # Initialize writer as None, it will be set after fetching headers

        try:
            # Initialize the scroll
            page = es.search(
                index=config["indices"],
                scroll='2m',  # Keep the scroll context for 2 minutes
                size=1000,  # Number of results per "page"
                body=query
            )
            
            scroll_size = page['hits']['total']['value']
            scroll_id = page['_scroll_id']

            while scroll_size > 0:
                if not writer:  # If writer is not set, define headers and initialize DictWriter
                    if page['hits']['hits']:
                        headers = page['hits']['hits'][0]['_source'].keys()
                        writer = csv.DictWriter(file, fieldnames=headers)
                        writer.writeheader()
                
                for hit in page['hits']['hits']:
                    row = {field: hit['_source'].get(field, '') for field in headers}
                    writer.writerow(row)

                page = es.scroll(scroll_id=scroll_id, scroll='2m')
                scroll_id = page['_scroll_id']
                scroll_size = len(page['hits']['hits'])

            es.clear_scroll(scroll_id=scroll_id)

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            traceback.print_exc()

print("Data extraction complete. Output is available in", output_csv_file)
