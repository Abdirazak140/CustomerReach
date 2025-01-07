import sqlite3
import os
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../db.sqlite3")

class ItemType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"

def initialize_database():
    """Initialize the SQLite database with the required schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            location TEXT,
            duration INTEGER,
            is_available BOOLEAN DEFAULT TRUE,
            item_type TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def handle_product_data(data):
    """Process product/service-related requests from RabbitMQ."""
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
            return {"status": "error", "message": "Invalid request type"}

def create_item(payload):
    if not payload:
        return {"status": "error", "message": "Payload is required"}

    if payload.get("item_type") == "service" and payload.get("duration") is None:
        return {"status": "error", "message": "Duration is required for services"}

    item_id = str(uuid4())
    current_time = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO items (id, name, description, price, category, location, duration, is_available, item_type, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id,
            payload.get("name"),
            payload.get("description"),
            payload.get("price"),
            payload.get("category"),
            payload.get("location"),
            payload.get("duration"),
            payload.get("is_available", True),
            payload.get("item_type"),
            current_time,
            current_time
        ))
        conn.commit()
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

    conn.close()
    return {"status": "success", "item_id": item_id}

def get_all_items(payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    item_type = payload.get("item_type") if payload else None
    skip = payload.get("skip", 0)
    limit = payload.get("limit", 100)

    try:
        if item_type:
            cursor.execute("""
                SELECT * FROM items WHERE item_type = ? LIMIT ? OFFSET ?
            """, (item_type, limit, skip))
        else:
            cursor.execute("""
                SELECT * FROM items LIMIT ? OFFSET ?
            """, (limit, skip))

        items = cursor.fetchall()
        conn.close()

        # Convert fetched data into a list of dictionaries
        item_list = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "category": row[4],
                "location": row[5],
                "duration": row[6],
                "is_available": row[7],
                "item_type": row[8],
                "created_at": row[9],
                "updated_at": row[10],
            }
            for row in items
        ]
        return {"status": "success", "items": item_list}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

def get_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {"status": "error", "message": "Item not found"}

        item = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "category": row[4],
            "location": row[5],
            "duration": row[6],
            "is_available": row[7],
            "item_type": row[8],
            "created_at": row[9],
            "updated_at": row[10],
        }
        return {"status": "success", "item": item}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

def update_item(item_id, payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Update the item
        update_fields = ", ".join(f"{key} = ?" for key in payload.keys())
        values = list(payload.values()) + [item_id]

        cursor.execute(f"""
            UPDATE items SET {update_fields}, updated_at = ? WHERE id = ?
        """, (*values, datetime.utcnow().isoformat(), item_id))
        conn.commit()
        conn.close()

        return {"status": "success", "message": "Item updated successfully"}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

def delete_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Item deleted successfully"}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

# Initialize the database schema on module load
initialize_database()
