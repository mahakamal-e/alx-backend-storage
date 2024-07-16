#!/usr/bin/env python3

"""
Retrieves statistics about Nginx logs stored in MongoDB.
"""

import pymongo


def get_stats(mongo_collection):
    """
    Retrieves statistics about Nginx logs stored in MongoDB.

    Args:
    - mongo_collection: PyMongo collection object representing the 'nginx' collection.

    Returns:
    - total_logs: Total number of documents in the 'nginx' collection.
    - method_counts: Dictionary with counts for each HTTP method ('GET', 'POST', 'PUT', 'PATCH', 'DELETE').
    - status_check_count: Number of documents where method='GET' and path='/status'.
    """
    total_logs = mongo_collection.count_documents({})
    
    method_counts = {
        "GET": mongo_collection.count_documents({"method": "GET"}),
        "POST": mongo_collection.count_documents({"method": "POST"}),
        "PUT": mongo_collection.count_documents({"method": "PUT"}),
        "PATCH": mongo_collection.count_documents({"method": "PATCH"}),
        "DELETE": mongo_collection.count_documents({"method": "DELETE"})
    }
    
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    
    return total_logs, method_counts, status_check_count


def main():
    """
    Main function to connect to MongoDB, retrieve statistics, and print them in the specified format.
    """
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["logs"]
        collection = db["nginx"]

        total_logs, method_counts, status_check_count = get_stats(collection)

        print(f"{total_logs} logs")
        print("Methods:")
        for method, count in method_counts.items():
            print(f"\tmethod {method}: {count}")
        print(f"{status_check_count} status check")

    except Exception as e:
        print(f"Error: {e}")
