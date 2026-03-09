"""
API routes for tech stack items (landing page logos).
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from bson.errors import InvalidId
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from models import TechStackItemCreate, TechStackItemUpdate
from database import get_tech_stack_collection
from auth import verify_admin_password

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=5)


def convert_doc(doc):
    if not doc:
        return None
    out = doc.copy()
    if "_id" in out:
        out["id"] = str(out["_id"])
        del out["_id"]
    if "created_at" in out and isinstance(out["created_at"], datetime):
        out["created_at"] = out["created_at"].isoformat()
    return out


@router.get("/tech-stack")
async def get_tech_stack():
    """Get all tech stack items, sorted by order then creation."""
    try:
        collection = get_tech_stack_collection()
        if collection is None:
            return []

        def fetch():
            items = list(collection.find({}))
            items.sort(key=lambda x: (x.get("order", 999), x.get("created_at", datetime.min.replace(tzinfo=timezone.utc))))
            return [convert_doc(d) for d in items]

        result = await asyncio.get_event_loop().run_in_executor(executor, fetch)
        return result
    except Exception as e:
        print(f"[ERROR] get_tech_stack: {e}")
        return []


@router.post("/tech-stack", status_code=status.HTTP_201_CREATED)
async def create_tech_stack_item(
    item: TechStackItemCreate,
    admin: bool = Depends(verify_admin_password),
):
    """Create a tech stack item. Requires admin."""
    try:
        collection = get_tech_stack_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available",
            )

        def insert():
            data = item.model_dump()
            data["order"] = collection.count_documents({})
            data["created_at"] = datetime.now(timezone.utc)
            r = collection.insert_one(data)
            doc = collection.find_one({"_id": r.inserted_id})
            return convert_doc(doc)

        created = await asyncio.get_event_loop().run_in_executor(executor, insert)
        return {"message": "Tech stack item created", "item": created}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] create_tech_stack: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tech-stack/{item_id}")
async def update_tech_stack_item(
    item_id: str,
    payload: TechStackItemUpdate,
    admin: bool = Depends(verify_admin_password),
):
    """Update a tech stack item. Requires admin."""
    try:
        collection = get_tech_stack_collection()
        if collection is None:
            raise HTTPException(status_code=503, detail="Database is not available")

        try:
            oid = ObjectId(item_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        def update():
            r = collection.update_one({"_id": oid}, {"$set": update_data})
            if r.matched_count == 0:
                return None
            return convert_doc(collection.find_one({"_id": oid}))

        result = await asyncio.get_event_loop().run_in_executor(executor, update)
        if result is None:
            raise HTTPException(status_code=404, detail="Tech stack item not found")
        return {"message": "Tech stack item updated", "item": result}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] update_tech_stack: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tech-stack/{item_id}")
async def delete_tech_stack_item(
    item_id: str,
    admin: bool = Depends(verify_admin_password),
):
    """Delete a tech stack item. Requires admin."""
    try:
        collection = get_tech_stack_collection()
        if collection is None:
            raise HTTPException(status_code=503, detail="Database is not available")

        try:
            oid = ObjectId(item_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")

        def delete():
            r = collection.delete_one({"_id": oid})
            return r.deleted_count > 0

        deleted = await asyncio.get_event_loop().run_in_executor(executor, delete)
        if not deleted:
            raise HTTPException(status_code=404, detail="Tech stack item not found")
        return {"message": "Tech stack item deleted"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] delete_tech_stack: {e}")
        raise HTTPException(status_code=500, detail=str(e))
