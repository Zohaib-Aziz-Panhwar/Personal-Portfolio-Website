"""
API routes for blog management.
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId
from bson.errors import InvalidId

from models import BlogCreate, BlogUpdate
from database import get_blogs_collection
from auth import verify_admin_password

# Create router instance
router = APIRouter()

# Thread pool executor for running pymongo operations
executor = ThreadPoolExecutor(max_workers=5)


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


@router.get("/blog")
async def get_blogs():
    """
    Get all blogs.
    Returns list of all blogs sorted by published_date or created_at (newest first).
    """
    try:
        collection = get_blogs_collection()
        if collection is None:
            print("[ERROR] Blogs collection is None - database not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def fetch_blogs():
            try:
                blogs = list(collection.find({}))
                # Sort by published_date if available, otherwise by created_at
                def get_sort_key(blog):
                    # Try published_date first (could be string or datetime)
                    pub_date = blog.get("published_date")
                    if pub_date:
                        if isinstance(pub_date, str):
                            try:
                                # Parse string date (YYYY-MM-DD format) to datetime for comparison
                                return datetime.strptime(pub_date, "%Y-%m-%d")
                            except (ValueError, TypeError):
                                # If parsing fails, fall through to created_at
                                pass
                        elif isinstance(pub_date, datetime):
                            return pub_date
                    
                    # Fall back to created_at
                    created = blog.get("created_at")
                    if isinstance(created, datetime):
                        return created
                    return datetime.min
                
                blogs.sort(key=get_sort_key, reverse=True)
                result = []
                for blog in blogs:
                    try:
                        converted = convert_objectid_to_str(blog)
                        result.append(converted)
                    except Exception as e:
                        print(f"[WARNING] Failed to convert blog {blog.get('_id', 'unknown')}: {e}")
                        converted = blog.copy() if blog else {}
                        if "_id" in converted:
                            converted["id"] = str(converted["_id"])
                            del converted["_id"]
                        if "created_at" in converted:
                            if isinstance(converted["created_at"], datetime):
                                converted["created_at"] = converted["created_at"].isoformat()
                        result.append(converted)
                return result
            except Exception as e:
                print(f"[ERROR] Error in fetch_blogs: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        blogs = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_blogs
        )
        print(f"[INFO] Successfully fetched {len(blogs)} blogs")
        return blogs
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to fetch blogs: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch blogs: {error_msg}"
        )


@router.get("/blog/{slug}")
async def get_blog_by_slug(slug: str):
    """
    Get a single blog by slug.
    """
    try:
        collection = get_blogs_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def fetch_blog():
            blog = collection.find_one({"slug": slug})
            return convert_objectid_to_str(blog) if blog else None
        
        blog = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_blog
        )
        
        if blog is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        return blog
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch blog: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch blog: {str(e)}"
        )


@router.post("/blog", status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Create a new blog post.
    Requires admin authentication.
    """
    try:
        collection = get_blogs_collection()
        if collection is None:
            print("[ERROR] Blogs collection is None - database not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            blog_dict = blog.model_dump()
            print(f"[INFO] Creating blog: {blog_dict.get('title')}")
        except Exception as e:
            print(f"[ERROR] Validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(e)}"
            )
        
        # Check if slug already exists
        def check_slug_exists():
            existing = collection.find_one({"slug": blog_dict.get("slug")})
            return existing is not None
        
        slug_exists = await asyncio.get_event_loop().run_in_executor(
            executor,
            check_slug_exists
        )
        
        if slug_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A blog with this slug already exists"
            )
        
        # Convert empty strings to None for optional fields
        for key in ['author', 'cover_image_url', 'published_date', 'reading_time']:
            if blog_dict.get(key) == '':
                blog_dict[key] = None
        
        # Ensure tags is a list
        if not isinstance(blog_dict.get('tags'), list):
            blog_dict['tags'] = []
        
        blog_dict["created_at"] = datetime.now(timezone.utc)
        
        def insert_blog():
            try:
                print(f"[INFO] Inserting blog into database...")
                result = collection.insert_one(blog_dict)
                print(f"[INFO] Blog inserted with ID: {result.inserted_id}")
                return str(result.inserted_id)
            except Exception as e:
                print(f"[ERROR] MongoDB insert error: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        blog_id = await asyncio.get_event_loop().run_in_executor(
            executor,
            insert_blog
        )
        
        def fetch_new_blog():
            try:
                blog = collection.find_one({"_id": ObjectId(blog_id)})
                if blog:
                    return convert_objectid_to_str(blog)
                return None
            except Exception as e:
                print(f"[ERROR] Error fetching new blog: {e}")
                return None
        
        new_blog = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_new_blog
        )
        
        if new_blog is None:
            print(f"[WARNING] Blog created but couldn't fetch it back")
            return {
                "message": "Blog created successfully",
                "blog_id": blog_id
            }
        
        print(f"[INFO] Blog created and fetched successfully")
        return {
            "message": "Blog created successfully",
            "blog": new_blog
        }
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to create blog: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create blog: {error_msg}"
        )


@router.put("/blog/{slug}")
async def update_blog(
    slug: str,
    blog_update: BlogUpdate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Update an existing blog post.
    Requires admin authentication.
    """
    try:
        collection = get_blogs_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        update_data = blog_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # If slug is being updated, check if new slug already exists
        if "slug" in update_data and update_data["slug"] != slug:
            def check_slug_exists():
                existing = collection.find_one({"slug": update_data["slug"]})
                return existing is not None
            
            slug_exists = await asyncio.get_event_loop().run_in_executor(
                executor,
                check_slug_exists
            )
            
            if slug_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A blog with this slug already exists"
                )
        
        def update_blog():
            result = collection.update_one(
                {"slug": slug},
                {"$set": update_data}
            )
            return result.modified_count > 0
        
        updated = await asyncio.get_event_loop().run_in_executor(
            executor,
            update_blog
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        # Fetch updated blog
        new_slug = update_data.get("slug", slug)
        def fetch_updated_blog():
            blog = collection.find_one({"slug": new_slug})
            return convert_objectid_to_str(blog) if blog else None
        
        updated_blog = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_updated_blog
        )
        
        return {
            "message": "Blog updated successfully",
            "blog": updated_blog
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to update blog: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update blog: {str(e)}"
        )


@router.delete("/blog/{slug}")
async def delete_blog(
    slug: str,
    admin: bool = Depends(verify_admin_password)
):
    """
    Delete a blog post.
    Requires admin authentication.
    """
    try:
        collection = get_blogs_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def delete_blog():
            result = collection.delete_one({"slug": slug})
            return result.deleted_count > 0
        
        deleted = await asyncio.get_event_loop().run_in_executor(
            executor,
            delete_blog
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        return {
            "message": "Blog deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to delete blog: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete blog: {str(e)}"
        )

