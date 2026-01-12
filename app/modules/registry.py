from fastapi import APIRouter

router = APIRouter()

@app.get("/list")
async def list_modules():
    return [
        {"id": "inbox", "name": "Inbox Cleaner", "icon": "envelope"},
        {"id": "ebay", "name": "eBay Watcher", "icon": "shopping-cart"},
        {"id": "social", "name": "Social Manager", "icon": "camera"}
    ]
