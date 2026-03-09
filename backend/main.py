"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import APP_NAME, APP_VERSION
from contact_routes import router as contact_router
from routes.projects_router import router as projects_router
from routes.blogs_router import router as blogs_router
from routes.certificates_router import router as certificates_router
from routes.education_router import router as education_router
from routes.site_settings_router import router as site_settings_router
from routes.tech_stack_router import router as tech_stack_router

# Create FastAPI app instance
app = FastAPI(
    title=APP_NAME,
    description="Backend API for portfolio website",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",  # React dev server (alternative)
        "http://127.0.0.1:5173",  # Vite dev server (alternative)
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(contact_router, prefix="/api", tags=["Contact"])
app.include_router(projects_router, prefix="/api", tags=["Projects"])
app.include_router(blogs_router, prefix="/api", tags=["Blogs"])
app.include_router(certificates_router, prefix="/api", tags=["Certificates"])
app.include_router(education_router, prefix="/api", tags=["Education"])
app.include_router(site_settings_router, prefix="/api", tags=["Site Settings"])
app.include_router(tech_stack_router, prefix="/api", tags=["Tech Stack"])


@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {
        "message": f"{APP_NAME} is running",
        "version": APP_VERSION,
        "docs": "/docs"
    }
