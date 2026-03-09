"""
Migration script to standardize image fields.
Copies image_url to cover_image for projects that don't have cover_image.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_projects_collection

def migrate_image_fields():
    """Copy image_url to cover_image for projects that don't have cover_image."""
    collection = get_projects_collection()
    
    if collection is None:
        print("[ERROR] Cannot connect to database. Please check your MongoDB connection.")
        return
    
    # Get all projects
    projects = list(collection.find({}))
    print(f"[INFO] Found {len(projects)} project(s).")
    
    migrated_count = 0
    
    for project in projects:
        image_url = project.get("image_url")
        cover_image = project.get("cover_image")
        
        # If project has image_url but no cover_image, copy it
        if image_url and not cover_image:
            try:
                result = collection.update_one(
                    {"_id": project["_id"]},
                    {"$set": {"cover_image": image_url}}
                )
                
                if result.modified_count > 0:
                    print(f"[SUCCESS] Migrated image for: '{project.get('title')}'")
                    migrated_count += 1
            except Exception as e:
                print(f"[ERROR] Error migrating project '{project.get('title')}': {e}")
        elif cover_image and not image_url:
            # If project has cover_image but no image_url, copy it for backward compatibility
            try:
                result = collection.update_one(
                    {"_id": project["_id"]},
                    {"$set": {"image_url": cover_image}}
                )
                
                if result.modified_count > 0:
                    print(f"[SUCCESS] Added image_url for: '{project.get('title')}'")
                    migrated_count += 1
            except Exception as e:
                print(f"[ERROR] Error updating project '{project.get('title')}': {e}")
        else:
            print(f"[SKIP] Project '{project.get('title')}' already has both fields or neither")
    
    print(f"\n[INFO] Migration complete. {migrated_count} project(s) updated.")


if __name__ == "__main__":
    print("Starting image field migration...")
    migrate_image_fields()
    print("Migration completed.")

