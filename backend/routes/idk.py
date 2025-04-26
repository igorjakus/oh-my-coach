from collections import OrderedDict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


items: OrderedDict[str, Item] = OrderedDict()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    items[item.name] = item
    return item


@app.get("/items/{item_name}", response_model=Item)
async def read_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]


@app.get("/items", response_model=list[Item])
async def read_items(limit: int = 10):
    return list(items.values())[:limit]


@app.delete("/items/{item_name}", response_model=Item)
async def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items.pop(item_name)
