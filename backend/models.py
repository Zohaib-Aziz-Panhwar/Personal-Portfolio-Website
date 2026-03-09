"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, HttpUrl
from typing import List, Optional
from datetime import datetime


class ContactRequest(BaseModel):
    """Model for contact form submission."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Contact person's name"
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )
    message: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Contact message (minimum 10 characters)"
    )
    
    @field_validator('message')
    @classmethod
    def validate_message_length(cls, v: str) -> str:
        """Validate that message is at least 10 characters long."""
        if len(v.strip()) < 10:
            raise ValueError("Message must be at least 10 characters long")
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "message": "This is a test message with at least 10 characters"
            }
        }
    }


class ContactResponse(BaseModel):
    """Model for contact form response."""
    
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: dict = Field(..., description="Submitted contact data")


class ProjectCreate(BaseModel):
    """Model for creating a new project."""
    
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200, pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$")
    short_description: str = Field(..., min_length=10, max_length=300)
    detailed_description: Optional[str] = Field(None, max_length=5000)
    tech_stack: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    github_link: Optional[str] = None
    live_demo: Optional[str] = None
    video_demo: Optional[str] = None
    problem_statement: Optional[str] = Field(None, max_length=2000)
    system_architecture: Optional[str] = Field(None, max_length=3000)
    key_features: List[str] = Field(default_factory=list)
    challenges: Optional[str] = Field(None, max_length=2000)
    solutions: Optional[str] = Field(None, max_length=2000)
    future_improvements: Optional[str] = Field(None, max_length=2000)
    cover_image: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Model for updating a project (all fields optional)."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200, pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$")
    short_description: Optional[str] = Field(None, min_length=10, max_length=300)
    detailed_description: Optional[str] = Field(None, max_length=5000)
    tech_stack: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    github_link: Optional[str] = None
    live_demo: Optional[str] = None
    video_demo: Optional[str] = None
    problem_statement: Optional[str] = Field(None, max_length=2000)
    system_architecture: Optional[str] = Field(None, max_length=3000)
    key_features: Optional[List[str]] = None
    challenges: Optional[str] = Field(None, max_length=2000)
    solutions: Optional[str] = Field(None, max_length=2000)
    future_improvements: Optional[str] = Field(None, max_length=2000)
    cover_image: Optional[str] = None


class BlogCreate(BaseModel):
    """Model for creating a new blog post."""
    
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200, pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$")
    short_description: str = Field(..., min_length=10, max_length=300)
    cover_image_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    author: Optional[str] = Field(None, max_length=100)
    published_date: Optional[str] = None  # ISO format date string (YYYY-MM-DD)
    reading_time: Optional[str] = Field(None, max_length=50)
    content: str = Field(..., min_length=50, max_length=50000)


class BlogUpdate(BaseModel):
    """Model for updating a blog post (all fields optional)."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200, pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$")
    short_description: Optional[str] = Field(None, min_length=10, max_length=300)
    cover_image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = Field(None, max_length=100)
    published_date: Optional[str] = None
    reading_time: Optional[str] = Field(None, max_length=50)
    content: Optional[str] = Field(None, min_length=50, max_length=50000)


class CertificateCreate(BaseModel):
    """Model for creating a new certificate."""
    
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    completion_month: int = Field(..., ge=1, le=12, description="Month of completion (1-12)")
    completion_year: int = Field(..., ge=1900, le=2100, description="Year of completion")
    short_description: str = Field(..., min_length=10, max_length=500)
    certificate_url: str = Field(..., description="URL to view the certificate")


class CertificateUpdate(BaseModel):
    """Model for updating a certificate (all fields optional)."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    completion_month: Optional[int] = Field(None, ge=1, le=12)
    completion_year: Optional[int] = Field(None, ge=1900, le=2100)
    short_description: Optional[str] = Field(None, min_length=10, max_length=500)
    certificate_url: Optional[str] = None


class EducationCreate(BaseModel):
    """Model for creating a new education entry."""
    
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    start_year: int = Field(..., ge=1900, le=2100, description="Start year")
    end_year: Optional[int] = Field(None, ge=1900, le=2100, description="End year (null for present)")
    details: Optional[str] = Field(None, max_length=500, description="Additional details")


class EducationUpdate(BaseModel):
    """Model for updating an education entry (all fields optional)."""
    
    degree: Optional[str] = Field(None, min_length=1, max_length=200)
    institution: Optional[str] = Field(None, min_length=1, max_length=200)
    start_year: Optional[int] = Field(None, ge=1900, le=2100)
    end_year: Optional[int] = Field(None, ge=1900, le=2100)
    details: Optional[str] = Field(None, max_length=500)


# --- Site settings (hero / landing page) ---

class SiteSettingsUpdate(BaseModel):
    """Model for updating site/hero settings (all fields optional)."""
    
    welcome_label: Optional[str] = Field(None, max_length=100)
    hero_name: Optional[str] = Field(None, max_length=200)
    hero_tagline: Optional[str] = Field(None, max_length=300)
    hero_description: Optional[str] = Field(None, max_length=2000)
    about_paragraph_1: Optional[str] = Field(None, max_length=2000)
    about_paragraph_2: Optional[str] = Field(None, max_length=2000)


# --- Tech stack (landing page logos) ---

class TechStackItemCreate(BaseModel):
    """Model for creating a tech stack item."""
    
    name: str = Field(..., min_length=1, max_length=100)
    logo_url: str = Field(..., min_length=1, max_length=2000, description="URL or path to logo image")


class TechStackItemUpdate(BaseModel):
    """Model for updating a tech stack item (all fields optional)."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    logo_url: Optional[str] = Field(None, min_length=1, max_length=2000)
    order: Optional[int] = Field(None, ge=0, description="Display order (lower first)")

