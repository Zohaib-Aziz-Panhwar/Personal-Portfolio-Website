"""
Seed site_settings (hero) and tech_stack for testing.
Run from backend directory: python scripts/seed_site_and_tech_stack.py
"""

import sys
import os
from datetime import datetime, timezone

# Allow importing from parent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_site_settings_collection, get_tech_stack_collection

DOC_ID = "hero"

DEFAULT_SETTINGS = {
    "_id": DOC_ID,
    "welcome_label": "WELCOME",
    "hero_name": "Zohaib Aziz Panhwar",
    "hero_tagline": "Developer · Researcher · Problem Solver",
    "hero_description": (
        "I'm a Computer Science student with a strong interest in AI automation "
        "and software development. I enjoy building practical solutions that "
        "simplify workflows, improve efficiency, and solve real-world problems."
    ),
}

# 2–4 tech stack items with logo URLs (devicon CDN + placeholder for N8N)
TECH_STACK_ITEMS = [
    {
        "name": "Python",
        "logo_url": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg",
        "order": 0,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "JavaScript",
        "logo_url": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
        "order": 1,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "N8N",
        "logo_url": "https://cdn.simpleicons.org/n8n/00C853",
        "order": 2,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Node.js",
        "logo_url": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original.svg",
        "order": 3,
        "created_at": datetime.now(timezone.utc),
    },
]


def seed():
    settings_coll = get_site_settings_collection()
    tech_coll = get_tech_stack_collection()

    if settings_coll is None or tech_coll is None:
        print("[ERROR] Database not available. Set MONGODB_URL and run from backend dir.")
        return False

    # Upsert site settings (one document with _id = DOC_ID)
    doc = settings_coll.find_one({"_id": DOC_ID})
    if not doc:
        settings_coll.insert_one(DEFAULT_SETTINGS)
    else:
        settings_coll.update_one(
            {"_id": DOC_ID},
            {"$set": {k: v for k, v in DEFAULT_SETTINGS.items() if k != "_id"}},
        )
    print("[INFO] Site settings (hero) seeded.")

    # Tech stack: only insert if empty
    if tech_coll.count_documents({}) == 0:
        tech_coll.insert_many(TECH_STACK_ITEMS)
        print(f"[INFO] Tech stack seeded with {len(TECH_STACK_ITEMS)} items.")
    else:
        print("[INFO] Tech stack already has data; skipping.")
    return True


if __name__ == "__main__":
    seed()
