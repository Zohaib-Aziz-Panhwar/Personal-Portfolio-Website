"""
API routes for project management.
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId
from bson.errors import InvalidId

from models import ProjectCreate, ProjectUpdate
from database import get_projects_collection
from auth import verify_admin_password

# Create router instance
router = APIRouter()

# Thread pool executor for running pymongo operations
executor = ThreadPoolExecutor(max_workers=5)


def convert_objectid_to_str(doc):
    """Convert MongoDB ObjectId to string and format dates."""
    if not doc:
        return doc
    # Create a copy to avoid modifying the original
    result = doc.copy()
    if "_id" in result:
        result["id"] = str(result["_id"])
        del result["_id"]
    if "created_at" in result:
        if isinstance(result["created_at"], datetime):
            # Convert datetime to ISO format string
            if result["created_at"].tzinfo is None:
                # Naive datetime - make it UTC
                result["created_at"] = result["created_at"].replace(tzinfo=timezone.utc).isoformat()
            else:
                # Timezone-aware datetime
                result["created_at"] = result["created_at"].isoformat()
    return result


@router.get("/projects")
async def get_projects():
    """
    Get all projects.
    Returns list of all projects sorted by creation date (newest first).
    """
    try:
        collection = get_projects_collection()
        if collection is None:
            print("[ERROR] Projects collection is None - database not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def fetch_projects():
            try:
                # Get all projects, try to sort by created_at
                projects = list(collection.find({}))
                # Sort manually to handle missing created_at
                projects.sort(key=lambda x: x.get("created_at", datetime.min), reverse=True)
                # Convert each project
                result = []
                for project in projects:
                    try:
                        converted = convert_objectid_to_str(project)
                        result.append(converted)
                    except Exception as e:
                        print(f"[WARNING] Failed to convert project {project.get('_id', 'unknown')}: {e}")
                        # Fallback conversion
                        converted = project.copy() if project else {}
                        if "_id" in converted:
                            converted["id"] = str(converted["_id"])
                            del converted["_id"]
                        if "created_at" in converted:
                            if isinstance(converted["created_at"], datetime):
                                converted["created_at"] = converted["created_at"].isoformat()
                        result.append(converted)
                return result
            except Exception as e:
                print(f"[ERROR] Error in fetch_projects: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        projects = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_projects
        )
        print(f"[INFO] Successfully fetched {len(projects)} projects")
        return projects
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to fetch projects: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch projects: {error_msg}"
        )


@router.get("/projects/{project_identifier}")
async def get_project(project_identifier: str):
    """
    Get a single project by ID or slug.
    """
    try:
        collection = get_projects_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def fetch_project():
            # Try to find by ObjectId first
            try:
                object_id = ObjectId(project_identifier)
                project = collection.find_one({"_id": object_id})
                if project:
                    return convert_objectid_to_str(project)
            except InvalidId:
                pass
            
            # If not found by ID, try to find by slug
            project = collection.find_one({"slug": project_identifier})
            return convert_objectid_to_str(project) if project else None
        
        project = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_project
        )
        
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return project
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch project: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch project: {str(e)}"
        )


@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Create a new project.
    Requires admin authentication.
    """
    try:
        collection = get_projects_collection()
        if collection is None:
            print("[ERROR] Projects collection is None - database not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        # Validate and prepare project data
        try:
            project_dict = project.model_dump()
            print(f"[INFO] Creating project: {project_dict.get('title')}")
        except Exception as e:
            print(f"[ERROR] Validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(e)}"
            )
        
        # Check if slug already exists
        def check_slug_exists():
            existing = collection.find_one({"slug": project_dict.get("slug")})
            return existing is not None
        
        slug_exists = await asyncio.get_event_loop().run_in_executor(
            executor,
            check_slug_exists
        )
        
        if slug_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Project with slug '{project_dict.get('slug')}' already exists"
            )
        
        # Convert empty strings to None for optional fields
        optional_fields = ['github_link', 'live_demo', 'video_demo', 'cover_image', 
                          'problem_statement', 'system_architecture', 'challenges', 
                          'solutions', 'future_improvements']
        for key in optional_fields:
            if project_dict.get(key) == '':
                project_dict[key] = None
        
        # Ensure lists are properly formatted
        for key in ['tech_stack', 'tools', 'key_features']:
            if not isinstance(project_dict.get(key), list):
                project_dict[key] = []
        
        project_dict["created_at"] = datetime.now(timezone.utc)
        
        def insert_project():
            try:
                print(f"[INFO] Inserting project into database...")
                result = collection.insert_one(project_dict)
                print(f"[INFO] Project inserted with ID: {result.inserted_id}")
                return str(result.inserted_id)
            except Exception as e:
                print(f"[ERROR] MongoDB insert error: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        project_id = await asyncio.get_event_loop().run_in_executor(
            executor,
            insert_project
        )
        
        # Fetch the created project to return it
        def fetch_new_project():
            try:
                project = collection.find_one({"_id": ObjectId(project_id)})
                if project:
                    return convert_objectid_to_str(project)
                return None
            except Exception as e:
                print(f"[ERROR] Error fetching new project: {e}")
                return None
        
        new_project = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_new_project
        )
        
        if new_project is None:
            # Project was created but we can't fetch it - return success with ID
            print(f"[WARNING] Project created but couldn't fetch it back")
            return {
                "message": "Project created successfully",
                "project_id": project_id
            }
        
        print(f"[INFO] Project created and fetched successfully")
        return {
            "message": "Project created successfully",
            "project": new_project
        }
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to create project: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {error_msg}"
        )


@router.put("/projects/{project_id}")
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Update an existing project.
    Requires admin authentication.
    """
    try:
        collection = get_projects_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        # Validate ObjectId format
        try:
            object_id = ObjectId(project_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid project ID format"
            )
        
        # Prepare update data (only include fields that are not None)
        update_data = project_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # If slug is being updated, check if it already exists (excluding current project)
        if "slug" in update_data:
            def check_slug_exists():
                existing = collection.find_one({
                    "slug": update_data["slug"],
                    "_id": {"$ne": object_id}
                })
                return existing is not None
            
            slug_exists = await asyncio.get_event_loop().run_in_executor(
                executor,
                check_slug_exists
            )
            
            if slug_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Project with slug '{update_data['slug']}' already exists"
                )
        
        # Convert empty strings to None for optional fields
        optional_fields = ['github_link', 'live_demo', 'video_demo', 'cover_image', 
                          'problem_statement', 'system_architecture', 'challenges', 
                          'solutions', 'future_improvements']
        for key in optional_fields:
            if key in update_data and update_data[key] == '':
                update_data[key] = None
        
        # Ensure lists are properly formatted
        for key in ['tech_stack', 'tools', 'key_features']:
            if key in update_data and not isinstance(update_data[key], list):
                update_data[key] = []
        
        def update_project():
            result = collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        
        updated = await asyncio.get_event_loop().run_in_executor(
            executor,
            update_project
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Fetch updated project
        def fetch_updated_project():
            project = collection.find_one({"_id": object_id})
            return convert_objectid_to_str(project) if project else None
        
        updated_project = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_updated_project
        )
        
        return {
            "message": "Project updated successfully",
            "project": updated_project
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to update project: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update project: {str(e)}"
        )


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    admin: bool = Depends(verify_admin_password)
):
    """
    Delete a project.
    Requires admin authentication.
    """
    try:
        collection = get_projects_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        # Validate ObjectId format
        try:
            object_id = ObjectId(project_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid project ID format"
            )
        
        def delete_project():
            result = collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        
        deleted = await asyncio.get_event_loop().run_in_executor(
            executor,
            delete_project
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        return {
            "message": "Project deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to delete project: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete project: {str(e)}"
        )
