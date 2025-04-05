import os
import sqlite3
import uuid
from datetime import datetime
import json

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../db.sqlite3")

def initialize_database():
    """Initialize the SQLite database with the required schema for NLP data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS business_analysis (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            description TEXT NOT NULL,
            keywords TEXT NOT NULL,
            entities TEXT NOT NULL,
            categories TEXT NOT NULL,
            sentiment REAL,
            additional_info TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_matches (
            id TEXT PRIMARY KEY,
            business_analysis_id TEXT NOT NULL,
            match_data TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (business_analysis_id) REFERENCES business_analysis (id)
        )
    """)

    conn.commit()
    conn.close()

def handle_nlp_data(data):
    """Process NLP-related requests from RabbitMQ."""
    request_type = data.get("request_type")

    match request_type:
        case "store_analysis":
            return store_analysis(data)
        case "get_analysis":
            return get_analysis(data.get("business_id"))
        case "find_matches":
            return find_matches(data.get("analysis"), data.get("criteria"))
        case _:
            return {"status": "error", "message": "Invalid request type"}

def store_analysis(data):
    """Store a business analysis in the database."""
    try:
        analysis_id = str(uuid.uuid4())
        current_time = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO business_analysis (
                id, user_id, description, keywords, entities, categories, 
                sentiment, additional_info, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_id,
            data.get("user_id"),
            data.get("description"),
            json.dumps(data.get("keywords", {})),
            json.dumps(data.get("entities", [])),
            json.dumps(data.get("categories", [])),
            data.get("sentiment", 0.0),
            json.dumps(data.get("additional_info", {})),
            current_time,
            current_time
        ))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "analysis_id": analysis_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_analysis(business_id):
    """Retrieve a business analysis from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM business_analysis WHERE id = ?
        """, (business_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {"status": "error", "message": "Analysis not found"}
        
        analysis = {
            "id": row[0],
            "user_id": row[1],
            "description": row[2],
            "keywords": json.loads(row[3]),
            "entities": json.loads(row[4]),
            "categories": json.loads(row[5]),
            "sentiment": row[6],
            "additional_info": json.loads(row[7]),
            "created_at": row[8],
            "updated_at": row[9]
        }
        
        return {"status": "success", "analysis": analysis}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def find_matches(analysis, criteria):
    """Find potential customer matches based on analysis and criteria."""
    # This is a simplified version - in a real implementation, you would:
    # 1. Query a customer database based on the criteria
    # 2. Apply NLP matching algorithms to find the best fits
    # 3. Return ranked results
    
    # For demonstration purposes, we'll return mock data
    matches = [
        {
            "id": str(uuid.uuid4()),
            "name": "Acme Corporation",
            "match_score": 0.85,
            "match_reasons": ["industry overlap", "keyword match: retail"],
            "contact_info": {
                "email": "contact@acmecorp.example",
                "phone": "555-123-4567"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "TechSolutions Inc.",
            "match_score": 0.72,
            "match_reasons": ["similar business size", "keyword match: digital"],
            "contact_info": {
                "email": "info@techsolutions.example",
                "phone": "555-987-6543"
            }
        }
    ]
    
    # Store the matches in the database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        match_id = str(uuid.uuid4())
        current_time = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO customer_matches (id, business_analysis_id, match_data, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            match_id,
            analysis.get("id"),
            json.dumps(matches),
            current_time
        ))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "matches": matches}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Initialize the database schema on module load
initialize_database()