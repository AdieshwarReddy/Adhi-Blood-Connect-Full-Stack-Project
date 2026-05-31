from bson import ObjectId
from datetime import datetime
from typing import Any, Dict, List, Union

def clean_db_doc(doc: Union[Dict[str, Any], None]) -> Union[Dict[str, Any], None]:
    """
    Translates a raw MongoDB BSON document to a frontend-friendly dictionary.
    Converts ObjectId fields to strings and maps _id to id.
    """
    if doc is None:
        return None
    
    cleaned = dict(doc)
    
    # Map _id -> id
    if "_id" in cleaned:
        cleaned["id"] = str(cleaned["_id"])
        del cleaned["_id"]
        
    # Standardize field transformations recursively
    for key, value in cleaned.items():
        if isinstance(value, ObjectId):
            cleaned[key] = str(value)
        elif isinstance(value, datetime):
            cleaned[key] = value.isoformat()
        elif isinstance(value, dict):
            cleaned[key] = clean_db_doc(value)
        elif isinstance(value, list):
            cleaned[key] = [
                clean_db_doc(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item 
                for item in value
            ]
            
    return cleaned

def clean_db_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Applies clean_db_doc to a list of MongoDB documents.
    """
    return [clean_db_doc(doc) for doc in docs if doc]
