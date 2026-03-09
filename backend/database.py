"""
MongoDB database connection using pymongo.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGODB_URL, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME

# Initialize MongoDB client and collection
client = None
db = None
contacts_collection = None

if MONGODB_URL:
    try:
        # Create MongoDB client
        client = MongoClient(MONGODB_URL)
        
        # Test the connection
        client.admin.command('ping')
        
        # Connect to the database
        db = client[MONGODB_DB_NAME]
        
        # Get the contacts collection
        contacts_collection = db[MONGODB_COLLECTION_NAME]
        
        print(f"[INFO] Connected to MongoDB. Database: {MONGODB_DB_NAME}, Collection: {MONGODB_COLLECTION_NAME}")
    except ConnectionFailure as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        client = None
    except Exception as e:
        print(f"[ERROR] MongoDB initialization error: {e}")
        client = None
else:
    print("[WARNING] MONGODB_URL not found in environment variables. MongoDB features will be disabled.")


def get_contacts_collection():
    """Get the contacts collection. Returns None if MongoDB is not configured."""
    return contacts_collection


def get_projects_collection():
    """Get the projects collection. Returns None if MongoDB is not configured."""
    if db is None:
        return None
    return db["projects"]


def get_blogs_collection():
    """Get the blogs collection. Returns None if MongoDB is not configured."""
    if db is None:
        return None
    return db["blogs"]


def get_certificates_collection():
    """Get the certificates collection. Returns None if MongoDB is not configured."""
    if db is None:
        return None
    return db["certificates"]


def get_education_collection():
    """Get the education collection. Returns None if MongoDB is not configured."""
    if db is None:
        return None
    return db["education"]


def get_site_settings_collection():
    """Get the site_settings collection (single-doc hero/landing content)."""
    if db is None:
        return None
    return db["site_settings"]


def get_tech_stack_collection():
    """Get the tech_stack collection (landing page tech logos)."""
    if db is None:
        return None
    return db["tech_stack"]

