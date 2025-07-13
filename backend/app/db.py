import os
from typing import List, Optional
from pymongo import MongoClient, UpdateOne
from pymongo.errors import ConnectionFailure
from pymongo.collection import Collection
from pymongo.results import BulkWriteResult
from dotenv import load_dotenv

load_dotenv()

MONGO_URI: str = os.getenv("MONGO_URI")
DB_NAME: str = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME")

class MongoDBClient:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self._verify_connection()
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def _verify_connection(self) -> None:
        try:
            self.client.server_info()
            print("[✓] Connected to MongoDB")
        except ConnectionFailure as e:
            print("[✗] MongoDB connection failed:", e)
            raise

    def save_architectures_upsert(self, parsed_list: List[dict]) -> Optional[BulkWriteResult]:
        """
        Bulk upsert multiple architecture documents.
        Insert if 'name' does not exist yet (avoid duplicates by 'name').
        """
        if not parsed_list:
            return None

        operations = []
        for doc in parsed_list:
            filter_ = {"name": doc.get("name")}
            update = {"$setOnInsert": doc}  # insert only if not exists
            operations.append(UpdateOne(filter_, update, upsert=True))

        if not operations:
            return None

        result = self.collection.bulk_write(operations)
        print(f"[✓] Bulk upsert completed: {result.bulk_api_result}")
        return result

    def get_architectures(self, limit: int = 0) -> List[dict]:
        """
        Retrieve saved architectures sorted by timestamp descending,
        excluding MongoDB internal _id.
        """
        cursor = self.collection.find({}, {"_id": 0}).sort("timestamp", -1)
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)

# Singleton Mongo client instance
mongo_client = MongoDBClient(MONGO_URI, DB_NAME, COLLECTION_NAME)

def save_architectures_upsert(parsed_list: List[dict]) -> Optional[BulkWriteResult]:
    return mongo_client.save_architectures_upsert(parsed_list)

def get_architectures(limit: int = 0) -> List[dict]:
    return mongo_client.get_architectures(limit)
