"""
API routes for education management.
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId
from bson.errors import InvalidId

from models import EducationCreate, EducationUpdate
from database import get_education_collection
from auth import verify_admin_password

# Create router instance
router = APIRouter()

# Thread pool executor for running pymongo operations
executor = ThreadPoolExecutor(max_workers=5)

# Maximum number of education entries to keep
MAX_EDUCATION_ENTRIES = 3


def convert_objectid_to_str(doc):
    """Convert MongoDB ObjectId to string and format dates."""
    if not doc:
        return doc
    result = doc.copy()
    if "_id" in result:
        result["id"] = str(result["_id"])
        del result["_id"]
    if "created_at" in result:
        if isinstance(result["created_at"], datetime):
            if result["created_at"].tzinfo is None:
                result["created_at"] = result["created_at"].replace(tzinfo=timezone.utc).isoformat()
            else:
                result["created_at"] = result["created_at"].isoformat()
    return result


@router.get("/education")
async def get_education():
    """
    Get all education entries.
    Returns list of all education entries sorted by start year (newest first).
    Only returns the latest 3 entries.
    """
    try:
        collection = get_education_collection()
        if collection is None:
            print("[ERROR] Education collection is None - database not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def fetch_education():
            try:
                education_list = list(collection.find({}))
                # Sort by created_at (newest first) so newly added entries appear on top
                # Then by start_year as secondary sort
                education_list.sort(
                    key=lambda x: (
                        x.get("created_at", datetime.min.replace(tzinfo=timezone.utc)),
                        x.get("start_year", 0),
                        x.get("end_year") if x.get("end_year") else 9999  # Present entries go first
                    ),
                    reverse=True
                )
                # Only return the latest 3
                education_list = education_list[:MAX_EDUCATION_ENTRIES]
                
                result = []
                for edu in education_list:
                    try:
                        converted = convert_objectid_to_str(edu)
                        result.append(converted)
                    except Exception as e:
                        print(f"[WARNING] Failed to convert education {edu.get('_id', 'unknown')}: {e}")
                        converted = edu.copy() if edu else {}
                        if "_id" in converted:
                            converted["id"] = str(converted["_id"])
                            del converted["_id"]
                        if "created_at" in converted:
                            if isinstance(converted["created_at"], datetime):
                                converted["created_at"] = converted["created_at"].isoformat()
                        result.append(converted)
                return result
            except Exception as e:
                print(f"[ERROR] Error in fetch_education: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        education = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_education
        )
        print(f"[INFO] Successfully fetched {len(education)} education entries")
        return education
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to fetch education: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch education: {error_msg}"
        )


@router.get("/education/{education_id}")
async def get_education_entry(education_id: str):
    """
    Get a single education entry by ID.
    """
    try:
        collection = get_education_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            object_id = ObjectId(education_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid education ID format"
            )
        
        def fetch_education():
            education = collection.find_one({"_id": object_id})
            return convert_objectid_to_str(education) if education else None
        
        education = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_education
        )
        
        if education is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education entry not found"
            )
        
        return education
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch education entry: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch education entry: {str(e)}"
        )


@router.post("/education", status_code=status.HTTP_201_CREATED)
async def create_education(
    education: EducationCreate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Create a new education entry.
    Requires admin authentication.
    Automatically deletes the oldest entry if there are already 3 entries.
    """
    try:
        collection = get_education_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            education_dict = education.model_dump()
            print(f"[INFO] Creating education entry: {education_dict.get('degree')}")
        except Exception as e:
            print(f"[ERROR] Validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(e)}"
            )
        
        education_dict["created_at"] = datetime.now(timezone.utc)
        
        def insert_education():
            try:
                # First, check how many entries exist
                count = collection.count_documents({})
                
                # If we have 3 or more entries, delete the oldest one (by created_at)
                if count >= MAX_EDUCATION_ENTRIES:
                    # Get all entries sorted by created_at (oldest first)
                    all_entries = list(collection.find({}))
                    all_entries.sort(
                        key=lambda x: x.get("created_at", datetime.min.replace(tzinfo=timezone.utc))
                    )
                    # Delete the oldest entry (first one added)
                    if all_entries:
                        oldest_id = all_entries[0].get("_id")
                        collection.delete_one({"_id": oldest_id})
                        print(f"[INFO] Deleted oldest education entry (by created_at) to maintain limit of {MAX_EDUCATION_ENTRIES}")
                
                # Insert the new entry
                result = collection.insert_one(education_dict)
                return str(result.inserted_id)
            except Exception as e:
                print(f"[ERROR] MongoDB insert error: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        edu_id = await asyncio.get_event_loop().run_in_executor(
            executor,
            insert_education
        )
        
        def fetch_new_education():
            try:
                edu = collection.find_one({"_id": ObjectId(edu_id)})
                if edu:
                    return convert_objectid_to_str(edu)
                return None
            except Exception as e:
                print(f"[ERROR] Error fetching new education entry: {e}")
                return None
        
        new_education = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_new_education
        )
        
        if new_education is None:
            return {
                "message": "Education entry created successfully",
                "education_id": edu_id
            }
        
        return {
            "message": "Education entry created successfully",
            "education": new_education
        }
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to create education entry: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create education entry: {error_msg}"
        )


@router.put("/education/{education_id}")
async def update_education(
    education_id: str,
    education_update: EducationUpdate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Update an existing education entry.
    Requires admin authentication.
    """
    try:
        collection = get_education_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            object_id = ObjectId(education_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid education ID format"
            )
        
        update_data = education_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        def update_education():
            result = collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        
        updated = await asyncio.get_event_loop().run_in_executor(
            executor,
            update_education
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education entry not found"
            )
        
        def fetch_updated_education():
            edu = collection.find_one({"_id": object_id})
            return convert_objectid_to_str(edu) if edu else None
        
        updated_education = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_updated_education
        )
        
        return {
            "message": "Education entry updated successfully",
            "education": updated_education
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to update education entry: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update education entry: {str(e)}"
        )


@router.delete("/education/{education_id}")
async def delete_education(
    education_id: str,
    admin: bool = Depends(verify_admin_password)
):
    """
    Delete an education entry.
    Requires admin authentication.
    """
    try:
        collection = get_education_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            object_id = ObjectId(education_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid education ID format"
            )
        
        def delete_education():
            result = collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        
        deleted = await asyncio.get_event_loop().run_in_executor(
            executor,
            delete_education
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education entry not found"
            )
        
        return {
            "message": "Education entry deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to delete education entry: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete education entry: {str(e)}"
        )

