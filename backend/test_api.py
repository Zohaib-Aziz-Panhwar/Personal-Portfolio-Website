"""
Simple script to test the projects API endpoint.
Run this to verify the backend is working correctly.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_get_projects():
    """Test GET /api/projects endpoint."""
    try:
        print("Testing GET /api/projects...")
        response = requests.get(f"{BASE_URL}/projects")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Found {len(data)} projects")
            if data:
                print(f"First project: {data[0].get('title', 'N/A')}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend server. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_create_project():
    """Test POST /api/projects endpoint."""
    try:
        print("\nTesting POST /api/projects...")
        test_project = {
            "title": "Test Project",
            "short_description": "This is a test project to verify the API is working correctly.",
            "full_description": "This is a comprehensive test project description that should be at least 50 characters long to pass validation.",
            "tech_stack": ["Python", "FastAPI", "MongoDB"],
            "github_link": "https://github.com/test/test",
            "image_url": "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800",
            "features": ["Feature 1", "Feature 2"]
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Admin-Password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/projects", json=test_project, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Success! Project created with ID: {data.get('project', {}).get('id', 'N/A')}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("API Test Script")
    print("=" * 50)
    
    # Test GET
    get_success = test_get_projects()
    
    # Test POST
    post_success = test_create_project()
    
    print("\n" + "=" * 50)
    if get_success and post_success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Check the errors above.")
    print("=" * 50)

