"""
Script to update existing projects with detailed descriptions.
This script adds detailed_description field to projects that don't have it.
"""

import sys
import os
from datetime import datetime, timezone

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_projects_collection

def update_existing_projects():
    """Update existing projects with detailed descriptions."""
    collection = get_projects_collection()
    
    if collection is None:
        print("[ERROR] Cannot connect to database. Please check your MongoDB connection.")
        return
    
    # Get all existing projects
    projects = list(collection.find({}))
    print(f"[INFO] Found {len(projects)} existing project(s).")
    
    # Detailed descriptions for common project types
    detailed_descriptions = {
        "portfolio": """This personal portfolio website showcases my work, skills, and experience as a developer. Built with modern web technologies, it provides a comprehensive view of my projects, technical expertise, and professional journey.

The portfolio features a responsive design that works seamlessly across all devices, from mobile phones to desktop computers. The clean, modern interface makes it easy for visitors to explore my work and learn about my technical capabilities.

Key highlights include a project showcase section where visitors can view detailed information about each project, including technologies used, features implemented, and links to live demos and source code. The portfolio also includes sections for skills, experience, and contact information.

The website is built with performance in mind, using optimized images, lazy loading, and efficient code to ensure fast load times. The codebase is well-structured and maintainable, following best practices for modern web development.""",

        "eco-track": """EcoTrack is an environmental monitoring and tracking application designed to help users understand and reduce their carbon footprint. The platform provides tools for tracking energy consumption, waste production, and transportation habits.

The application features an intuitive dashboard that displays environmental impact metrics in an easy-to-understand format. Users can input data about their daily activities, and the system calculates their carbon footprint based on industry-standard formulas.

One of the key features is the goal-setting functionality, which allows users to set targets for reducing their environmental impact. The system provides personalized recommendations based on user data, suggesting actionable steps to achieve these goals.

The platform includes social features that enable users to share their progress, participate in challenges, and connect with others who are committed to environmental sustainability. Leaderboards and achievements gamify the experience, making it more engaging for users.

Data visualization is a core component, with charts and graphs that show trends over time, helping users understand the impact of their lifestyle choices. The application also provides educational content about environmental issues and sustainable practices.""",

        "ecommerce": """This e-commerce platform is a full-featured online shopping solution that provides a seamless shopping experience for customers and powerful management tools for administrators.

The platform includes a comprehensive product catalog with advanced search and filtering capabilities. Products can be organized into categories, and each product page includes detailed descriptions, multiple images, customer reviews, and related product suggestions.

The shopping cart system supports multiple payment methods and provides a secure checkout process. Order management includes order tracking, status updates, and email notifications to keep customers informed throughout the purchase process.

For administrators, the platform offers a robust dashboard for managing products, orders, customers, and inventory. The admin panel includes analytics and reporting features that provide insights into sales performance, popular products, and customer behavior.

The platform is built with security as a priority, implementing secure payment processing, data encryption, and protection against common web vulnerabilities. User authentication and authorization ensure that sensitive operations are protected.""",

        "blog": """This blog platform is a content management system designed for writers and content creators. It provides a clean, distraction-free writing environment and a beautiful reading experience for visitors.

The platform features a rich text editor that supports formatting, images, code blocks, and embedded media. Posts can be organized using tags and categories, making it easy for readers to discover related content.

The reading experience is optimized for engagement, with features like reading time estimates, social sharing buttons, and related post suggestions. The design is responsive and accessible, ensuring that content is readable on all devices.

For content creators, the platform includes analytics that show post performance, reader engagement, and traffic sources. This data helps writers understand their audience and create content that resonates with readers.

The platform supports multiple authors, with role-based permissions that allow different levels of access. Comments and discussions can be enabled or disabled per post, giving authors control over engagement on their content.""",

        "task-manager": """This task management application helps individuals and teams organize their work and stay productive. It combines the simplicity of a to-do list with the power of project management tools.

The application features multiple views including list view, board view (Kanban), and calendar view, allowing users to work in the way that suits them best. Tasks can be organized into projects, assigned to team members, and tagged for easy filtering.

Collaboration features include comments, file attachments, and activity feeds that keep team members informed about project updates. Notifications ensure that important changes don't go unnoticed.

The application includes productivity features like recurring tasks, task templates, and time tracking. These tools help users work more efficiently and understand how they spend their time.

Reporting and analytics provide insights into productivity patterns, helping users identify areas for improvement. The application can generate reports on task completion rates, time spent on different projects, and team performance metrics."""
    }
    
    updated_count = 0
    
    for project in projects:
        project_title = project.get("title", "").lower()
        project_slug = project.get("slug", "").lower()
        
        # Check if project already has detailed_description
        if project.get("detailed_description"):
            print(f"[SKIP] Project '{project.get('title')}' already has detailed_description")
            continue
        
        # Try to match project with known descriptions
        detailed_description = None
        
        if "portfolio" in project_title or "portfolio" in project_slug:
            detailed_description = detailed_descriptions.get("portfolio")
        elif "eco" in project_title or "eco" in project_slug or "track" in project_slug:
            detailed_description = detailed_descriptions.get("eco-track")
        elif "ecommerce" in project_title or "ecommerce" in project_slug or "e-commerce" in project_slug:
            detailed_description = detailed_descriptions.get("ecommerce")
        elif "blog" in project_title or "blog" in project_slug:
            detailed_description = detailed_descriptions.get("blog")
        elif "task" in project_title or "task" in project_slug or "todo" in project_slug:
            detailed_description = detailed_descriptions.get("task-manager")
        
        # If no match found, create a generic description based on short_description
        if not detailed_description:
            short_desc = project.get("short_description", "")
            tech_stack = project.get("tech_stack", [])
            tech_list = ", ".join(tech_stack) if tech_stack else "modern web technologies"
            
            detailed_description = f"""This project is a comprehensive solution built with {tech_list}. {short_desc}

The application is designed with user experience and performance in mind, providing a smooth and intuitive interface. The architecture is scalable and maintainable, following industry best practices for code organization and structure.

Key aspects of the project include robust error handling, comprehensive testing, and thorough documentation. The codebase is well-structured, making it easy for developers to understand and contribute to the project.

The project demonstrates proficiency in modern development practices, including version control, code reviews, and continuous integration. Security considerations are built into every layer of the application, ensuring that user data is protected and the system is resilient against common vulnerabilities."""
        
        # Update the project
        try:
            result = collection.update_one(
                {"_id": project["_id"]},
                {"$set": {"detailed_description": detailed_description}}
            )
            
            if result.modified_count > 0:
                print(f"[SUCCESS] Updated project: '{project.get('title')}'")
                updated_count += 1
            else:
                print(f"[WARNING] Failed to update project: '{project.get('title')}'")
        except Exception as e:
            print(f"[ERROR] Error updating project '{project.get('title')}': {e}")
    
    print(f"\n[INFO] Update complete. {updated_count} project(s) updated with detailed descriptions.")


if __name__ == "__main__":
    print("Starting project update script...")
    update_existing_projects()
    print("Update script completed.")

