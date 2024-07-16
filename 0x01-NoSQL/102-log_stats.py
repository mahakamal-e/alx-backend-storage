#!/usr/bin/env python3
"""
Retrieves statistics about Nginx logs stored in MongoDB,
including methods count and top IPs.
"""
import pymongo
from collections import Counter


def get_stats(mongo_collection):
    """
    Retrieves statistics about Nginx logs stored in MongoDB.
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
    
    ip_counts = Counter(doc["ip"] for doc in mongo_collection.find({}, {"ip": 1}))
    
    return total_logs, method_counts, status_check_count, ip_counts

def main():
    """
    Main function to connect to MongoDB.
    """
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["logs"]
        collection = db["nginx"]

        total_logs, method_counts, status_check_count, ip_counts = get_stats(collection)

        print(f"{total_logs} logs")
        print("Methods:")
        for method, count in method_counts.items():
            print(f"\tmethod {method}: {count}")
        print(f"{status_check_count} status check")
        
        print("IPs:")
        sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for ip, count in sorted_ips:
            print(f"\t{ip}: {count}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
