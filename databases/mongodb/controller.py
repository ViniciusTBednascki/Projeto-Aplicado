from pymongo import MongoClient, InsertOne
from pymongo.errors import BulkWriteError, DuplicateKeyError
from typing import List, Dict, Any, Optional, Union
import os

class MongoDBController:
    def __init__(self, connection_uri: str = None, db_name: str = "bronze"):
        """
        Initialize MongoDB controller.
        Uses localhost:27017 by default for Docker setup.
        """
        self.uri = connection_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = db_name
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]
        
    def get_collection(self, collection_name: str):
        """Get collection instance."""
        return self.db[collection_name]
    
    def bulk_insert(self, collection_name: str, documents: List[Dict[str, Any]], ordered: bool = False) -> Dict[str, int]:
        """
        Bulk insert documents (optimized for large arrays >100k).
        Returns: {'inserted': int, 'errors': int}
        """
        collection = self.get_collection(collection_name)
        operations = [InsertOne(doc) for doc in documents]
        
        try:
            result = collection.bulk_write(operations, ordered=ordered)
            return {
                'inserted': result.inserted_count,
                'errors': 0
            }
        except BulkWriteError as bwe:
            return {
                'inserted': bwe.details.get('nInserted', 0),
                'errors': len(bwe.details.get('writeErrors', [])),
                'details': bwe.details
            }
    
    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert single document, return inserted ID."""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)
    
    def find(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Find documents with optional query and limit."""
        collection = self.get_collection(collection_name)
        query = query or {}
        cursor = collection.find(query)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find single document."""
        collection = self.get_collection(collection_name)
        return collection.find_one(query)
    
    def update_one(self, collection_name: str, filter_query: Dict[str, Any], 
                   update_query: Dict[str, Any], upsert: bool = False) -> int:
        """Update single document, return matched count."""
        collection = self.get_collection(collection_name)
        result = collection.update_one(filter_query, update_query, upsert=upsert)
        return result.matched_count
    
    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete single document, return deleted count."""
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result.deleted_count
    
    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete multiple documents."""
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        return result.deleted_count
    
    def get_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get collection stats."""
        collection = self.get_collection(collection_name)
        return collection.stats()
    
    def close(self):
        """Close connection."""
        self.client.close()