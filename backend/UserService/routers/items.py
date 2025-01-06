from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/api/items")

class ItemType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"

class ItemBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    location: str
    duration: Optional[int] = None
    is_available: bool = True
    item_type: ItemType

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[int] = None
    is_available: Optional[bool] = None
    item_type: Optional[ItemType] = None

class Item(ItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime



items = {}

#POST for product/services endpoint
@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    #Checkk if that service has duration cuz of optional stuffs
    if item.item_type == ItemType.SERVICE and item.duration is None:
        raise HTTPException(
            status_code=400,
            detail="Duration is required for services"
        )
    
    item_id = uuid4()
    current_time = datetime.utcnow()
    
    item_dict = item.dict()
    item_dict.update({
        "id": item_id,
        "created_at": current_time,
        "updated_at": current_time
    })
    
    items[item_id] = item_dict
    return item_dict

#GET all product/services endpoint
@router.get("/", response_model=List[Item])
async def get_all_items(
    skip: int = 0,
    limit: int = 100,
    item_type: Optional[ItemType] = None
):
    if item_type:
        filtered_items = [item for item in items.values() if item["item_type"] == item_type]
        return filtered_items[skip:skip + limit]
    return list(items.values())[skip:skip + limit]

#GET specific product/services endpoint
@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: UUID):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

#PUT to update product/services endpoint
@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: UUID, item_update: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stored_item = items[item_id]
    update_data = item_update.dict(exclude_unset=True)
    
    if (
        stored_item["item_type"] == ItemType.SERVICE
        and "duration" in update_data
        and update_data["duration"] is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Duration cannot be removed from services"
        )
    
    for field, value in update_data.items():
        if value is not None:
            stored_item[field] = value
    
    stored_item["updated_at"] = datetime.utcnow()
    return stored_item

#DELETE for product/services endpoint
@router.delete("/{item_id}")
async def delete_item(item_id: UUID):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items[item_id]
    return {"message": "Item deleted successfully"}