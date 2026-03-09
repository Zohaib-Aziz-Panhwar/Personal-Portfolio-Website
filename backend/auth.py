"""
Simple password-based authentication for admin endpoints.
"""

import os
from fastapi import HTTPException, status, Header
from typing import Optional

# Admin password from environment variable
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Change this in production!


def verify_admin_password(
    x_admin_password: Optional[str] = Header(None, alias="X-Admin-Password")
) -> bool:
    """
    Verify admin password from header.
    Returns True if password is correct, raises HTTPException otherwise.
    """
    if not x_admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin password required. Include 'X-Admin-Password' header."
        )
    
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin password"
        )
    
    return True

