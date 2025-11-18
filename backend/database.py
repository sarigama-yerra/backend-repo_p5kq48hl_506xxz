import os
from typing import Any, Dict, Iterable
from datetime import datetime
from pymongo import MongoClient

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "creative_agency")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


def create_document(collection_name: str, data: Dict[str, Any]):
    data = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    result = db[collection_name].insert_one(data)
    return result.inserted_id


def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> Iterable[Dict[str, Any]]:
    filter_dict = filter_dict or {}
    cursor = db[collection_name].find(filter_dict).limit(limit)
    for doc in cursor:
        doc.pop("_id", None)
        return_list = doc
        yield return_list
