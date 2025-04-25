# FastAPI Example

### Setup & Run
```bash
fastapi dev fastapi_example.py
```

### API Usage
Interactive docs available at: `localhost:8000/docs`

#### Create Item
```bash
curl -X POST localhost:8000/items \
-H "Content-Type: application/json" \
-d '{"name":"item1","price":10.5,"description":"test"}'
```

#### Get Item
```bash
curl localhost:8000/items/item1
```

#### List Items
```bash
curl localhost:8000/items
```

#### Delete Item
```bash
curl -X DELETE localhost:8000/items/item1
```
