"""
API routes for site/hero settings (landing page content).
Single document in site_settings collection with id "hero".
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId

from models import SiteSettingsUpdate
from database import get_site_settings_collection
from auth import verify_admin_password

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=5)

DOC_ID = "hero"

DEFAULT_SETTINGS = {
    "welcome_label": "WELCOME",
    "hero_name": "Zohaib Aziz Panhwar",
    "hero_tagline": "Developer · Researcher · Problem Solver",
    "hero_description": (
        "I'm a Computer Science student with a strong interest in AI automation "
        "and software development. I enjoy building practical solutions that "
        "simplify workflows, improve efficiency, and solve real-world problems."
    ),
    "about_paragraph_1": "",
    "about_paragraph_2": "",
}


def _get_settings_doc(collection):
    """Get the single settings document. Returns dict without _id or with id."""
    doc = collection.find_one({"_id": DOC_ID})
    if not doc:
        return None
    out = doc.copy()
    out["id"] = out.get("_id", DOC_ID)
    if "_id" in out:
        del out["_id"]
    return out


@router.get("/site-settings")
async def get_site_settings():
    """
    Get site/hero settings (public).
    Returns defaults if no document exists yet.
    """
    try:
        collection = get_site_settings_collection()
        if collection is None:
            return DEFAULT_SETTINGS

        def fetch():
            doc = collection.find_one({"_id": DOC_ID})
            if not doc:
                out = DEFAULT_SETTINGS.copy()
            else:
                out = {k: v for k, v in doc.items() if k != "_id"}
                for key, default_val in DEFAULT_SETTINGS.items():
                    if key not in out:
                        out[key] = default_val
            out["id"] = DOC_ID
            return out

        result = await asyncio.get_event_loop().run_in_executor(executor, fetch)
        return result
    except Exception as e:
        print(f"[ERROR] get_site_settings: {e}")
        return DEFAULT_SETTINGS


@router.put("/site-settings")
async def update_site_settings(
    payload: SiteSettingsUpdate,
    admin: bool = Depends(verify_admin_password),
):
    """
    Update site/hero settings. Requires admin auth.
    """
    try:
        collection = get_site_settings_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available",
            )

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update",
            )

        def upsert():
            collection.update_one(
                {"_id": DOC_ID},
                {"$set": update_data},
                upsert=True,
            )
            doc = collection.find_one({"_id": DOC_ID})
            out = {k: v for k, v in doc.items() if k != "_id"}
            out["id"] = DOC_ID
            return out

        result = await asyncio.get_event_loop().run_in_executor(executor, upsert)
        return {"message": "Site settings updated", "settings": result}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] update_site_settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
