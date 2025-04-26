from collections import OrderedDict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

idk_router = APIRouter()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


items: OrderedDict[str, Item] = OrderedDict()


@idk_router.get("/")
def root():
    return {"message": "Hello World"}


@idk_router.post("/items", response_model=Item)
async def create_item(item: Item):
    items[item.name] = item
    return item


@idk_router.get("/items/{item_name}", response_model=Item)
async def read_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]


@idk_router.get("/items", response_model=list[Item])
async def read_items(limit: int = 10):
    return list(items.values())[:limit]


@idk_router.delete("/items/{item_name}", response_model=Item)
async def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items.pop(item_name)
