# elasticquery.py

This python script has been rewritten from the ground up, in order to make it simpler for other engineers using it for log aggregation and testing. It is tailored for Cisco.IOS logs but can be easily adjusted for other types of logs.

# Features
- Query multiple Elasticsearch deployments with different Cloud ID's.
- Handles specific log phrases like "Login Success" and "Configured programmatically by process".
- Reads confgiuration from an external JSON file for flexibility.
- Paginated fetching of logs to handle large data sets.
- Writes query results to local JSON files for further analysis or ingestion.
- Logs progress and errors to a .log file for easy debugging.

# Requirements
- Python 3.x
- Elasticsearch Python library


# How to Run
1. Install necessary dependencies by utilizing 'pip install elasticsearch'.
2. Populate all necessary fields in the config.json, and change queries to your needs.
3. CD to your directory, and run the script with python.

# How it works
The script will query Elasticsearch 10,000 hits at a time using the point in time and search after features. Every 100,000 hits will be written to a file. Every 1,000,000 hits, those files will be appended to the archive.
