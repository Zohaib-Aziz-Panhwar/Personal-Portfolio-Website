"""
Script to seed the database with initial education data.
Run this script once to populate the education collection with sample data.
"""

import sys
from datetime import datetime, timezone
from database import get_education_collection

def seed_education():
    """Seed the education collection with initial data."""
    collection = get_education_collection()
    
    if collection is None:
        print("[ERROR] Education collection is None - database not available")
        print("Make sure MongoDB is running and MONGODB_URL is set in your .env file")
        return False
    
    # Check if data already exists
    existing_count = collection.count_documents({})
    if existing_count > 0:
        print(f"[INFO] Education collection already has {existing_count} entries.")
        response = input("Do you want to clear existing data and seed fresh data? (yes/no): ")
        if response.lower() == 'yes':
            collection.delete_many({})
            print("[INFO] Cleared existing education entries.")
        else:
            print("[INFO] Keeping existing data. Exiting.")
            return True
    
    # Sample education data (from the hardcoded values)
    education_data = [
        {
            "degree": "B.S Computer Science",
            "institution": "DHA Suffa University, Karachi",
            "start_year": 2024,
            "end_year": None,  # Present
            "details": "Focus: AI Automation and ML",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "degree": "Intermediate, Pre-Engineering",
            "institution": "Shah Abdul Latif College, Mirpurkhas",
            "start_year": 2021,
            "end_year": 2023,
            "details": "",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "degree": "Matriculation, Science",
            "institution": "The Vision High Sec School, Mirpurkhas",
            "start_year": 2019,
            "end_year": 2021,
            "details": "",
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    try:
        result = collection.insert_many(education_data)
        print(f"[SUCCESS] Successfully seeded {len(result.inserted_ids)} education entries:")
        for i, edu in enumerate(education_data, 1):
            period = f"{edu['start_year']} – PRESENT" if edu['end_year'] is None else f"{edu['start_year']} – {edu['end_year']}"
            print(f"  {i}. {edu['degree']} - {edu['institution']} ({period})")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to seed education data: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Education Data Seeding Script")
    print("=" * 60)
    success = seed_education()
    if success:
        print("\n[SUCCESS] Education seeding completed!")
    else:
        print("\n[ERROR] Education seeding failed!")
        sys.exit(1)

