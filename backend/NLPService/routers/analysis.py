from fastapi import APIRouter, HTTPException, Request, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
import spacy
from collections import Counter

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)

from common.rabbitmq import request_service_with_response, publish_message

router = APIRouter(prefix="/api/nlp")

# Load spaCy model - install: python -m spacy download en_core_web_md
nlp = spacy.load("en_core_web_md")

class BusinessAnalysisRequest(BaseModel):
    description: str
    additional_info: Optional[Dict[str, Any]] = None

class MatchRequest(BaseModel):
    business_id: str
    criteria: Dict[str, Any]

@router.post("/analyze")
async def analyze_business(request: Request, data: BusinessAnalysisRequest):
    """Analyze a business description using NLP techniques"""
    user_id = request.state.user.get("user_id")
    
    # Process the text with spaCy
    doc = nlp(data.description)
    
    # Extract keywords (nouns, proper nouns, and adjectives)
    keywords = [token.lemma_.lower() for token in doc if token.pos_ in ("NOUN", "PROPN", "ADJ") 
                and not token.is_stop and len(token.text) > 2]
    
    # Get keyword frequencies
    keyword_freq = Counter(keywords)
    top_keywords = keyword_freq.most_common(10)
    
    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Determine business categories based on keywords
    business_categories = determine_categories(keywords)
    
    # Calculate sentiment
    sentiment_score = doc.sentiment
    
    # Store analysis in database
    analysis_payload = {
        "request_type": "store_analysis",
        "user_id": user_id,
        "description": data.description,
        "keywords": dict(top_keywords),
        "entities": entities,
        "categories": business_categories,
        "sentiment": sentiment_score,
        "additional_info": data.additional_info
    }
    
    db_response = request_service_with_response("nlp_data", analysis_payload)
    
    if db_response.get("status") != "success":
        raise HTTPException(status_code=500, detail="Failed to store analysis")
    
    return {
        "keywords": dict(top_keywords),
        "entities": entities,
        "categories": business_categories,
        "sentiment": sentiment_score,
        "analysis_id": db_response.get("analysis_id")
    }

@router.post("/match")
async def match_customers(request: Request, data: MatchRequest):
    """Find potential customer matches based on business description and criteria"""
    user_id = request.state.user.get("user_id")
    
    # Get the business analysis
    analysis_payload = {
        "request_type": "get_analysis",
        "business_id": data.business_id
    }
    
    analysis = request_service_with_response("nlp_data", analysis_payload)
    
    if analysis.get("status") != "success":
        raise HTTPException(status_code=404, detail="Business analysis not found")
    
    match_payload = {
        "request_type": "find_matches",
        "analysis": analysis.get("analysis"),
        "criteria": data.criteria
    }
    
    matches = request_service_with_response("nlp_data", match_payload)
    
    if matches.get("status") != "success":
        raise HTTPException(status_code=500, detail="Failed to find matches")
    
    return {
        "matches": matches.get("matches"),
        "match_count": len(matches.get("matches", []))
    }

def determine_categories(keywords):
    """Simple function to determine business categories based on keywords"""
    categories = set()
    
    # Later we use a more sophisticated categorization
    category_keywords = {
        "retail": ["store", "shop", "retail", "sell", "product", "customer"],
        "technology": ["software", "tech", "digital", "computer", "app", "online"],
        "healthcare": ["health", "medical", "doctor", "patient", "care", "hospital"],
        "education": ["education", "school", "teach", "student", "learn", "training"],
        "finance": ["financial", "bank", "money", "investment", "finance", "fund"],
        "food": ["food", "restaurant", "eat", "drink", "meal", "catering"]
    }
    
    # Check for keyword matches
    for category, terms in category_keywords.items():
        if any(keyword in terms for keyword in keywords):
            categories.add(category)
    
    return list(categories) if categories else ["uncategorized"]