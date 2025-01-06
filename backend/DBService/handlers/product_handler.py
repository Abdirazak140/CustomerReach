import uuid
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional

items = {}

class ItemType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"

def validate_item_type(data):
    try:
        return ItemType(data["item_type"])
    except ValueError:
        return None

def handle_product_data(data):
    request_type = data.get("request_type")

    match request_type:
        case "create_item":
            return create_item(data.get("payload"))
        case "get_all_items":
            return get_all_items(data.get("payload"))
        case "get_item":
            return get_item(data.get("item_id"))
        case "update_item":
            return update_item(data.get("item_id"), data.get("payload"))
        case "delete_item":
            return delete_item(data.get("item_id"))
        case _:
            return {
                "status": "error", 
                "message": "Invalid request type"
                }

def create_item(payload):
    if not payload:
        return {
            "status": "error", 
            "message": "Payload is required"
            }

    if payload.get("item_type") == "service" and payload.get("duration") is None:
        return {
            "status": "error", 
            "message": "Duration is required for services"
            }

    item_id = uuid.uuid4()
    current_time = datetime.utcnow()

    item_dict = {
        "id": item_id,
        "name": payload.get("name"),
        "description": payload.get("description"),
        "price": payload.get("price"),
        "category": payload.get("category"),
        "location": payload.get("location"),
        "duration": payload.get("duration"),
        "is_available": payload.get("is_available", True),
        "item_type": payload.get("item_type"),
        "created_at": current_time,
        "updated_at": current_time,
    }

    items[item_id] = item_dict
    return {
        "status": "success", 
        "item": item_dict
        }

def get_all_items(payload):
    if not items:
        return {
            "status": "success", 
            "items": []
            }

    item_type = payload.get("item_type") if payload else None
    skip = payload.get("skip", 0)
    limit = payload.get("limit", 100)

    if item_type:
        filtered_items = [item for item in items.values() if item["item_type"] == item_type]
        return {
            "status": "success", 
            "items": filtered_items[skip:skip + limit]
            }

    return {
        "status": "success", 
        "items": list(items.values())[skip:skip + limit]
        }

def get_item(item_id):
    try:
        item_id = UUID(item_id)
    except ValueError:
        return {
            "status": "error", 
            "message": "Invalid item ID format"
            }

    item = items.get(item_id)
    if not item:
        return {
            "status": "error", 
            "message": "Item not found"
            }

    return {
        "status": "success", 
        "item": item
        }

def update_item(item_id, payload):
    try:
        item_id = UUID(item_id)
    except ValueError:
        return {
            "status": "error", 
            "message": "Invalid item ID format"
            }

    if item_id not in items:
        return {
            "status": "error", 
            "message": "Item not found"
            }

    stored_item = items[item_id]
    for field, value in payload.items():
        if field == "duration" and stored_item["item_type"] == "service" and value is None:
            return {
                "status": "error", 
                "message": "Duration cannot be removed from services"
                }
        if value is not None:
            stored_item[field] = value

    stored_item["updated_at"] = datetime.utcnow()
    return {
        "status": "success", 
        "item": stored_item
        }

def delete_item(item_id):
    try:
        item_id = UUID(item_id)
    except ValueError:
        return {
            "status": "error", 
            "message": "Invalid item ID format"
            }

    if item_id not in items:
        return {
            "status": "error", 
            "message": "Item not found"
            }

    del items[item_id]
    return {
        "status": "success", 
        "message": "Item deleted successfully"
        }
