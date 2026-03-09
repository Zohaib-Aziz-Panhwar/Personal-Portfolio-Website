"""
Seed script to populate the database with sample blog posts.
Run this script to add sample blogs to the database.
"""

import sys
import os
from datetime import datetime, timezone

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_blogs_collection

def seed_blogs():
    """Seed the database with sample blog posts."""
    collection = get_blogs_collection()
    
    if collection is None:
        print("[ERROR] Cannot connect to database. Please check your MongoDB connection.")
        return
    
    # Check if blogs already exist
    existing_count = collection.count_documents({})
    if existing_count > 0:
        print(f"[INFO] Database already contains {existing_count} blog(s).")
        print("[INFO] Adding sample blogs anyway to ensure we have enough for testing...")
    
    sample_blogs = [
        {
            "title": "How I Built My Portfolio Using React and Node.js",
            "slug": "how-i-built-my-portfolio-using-react-and-nodejs",
            "short_description": "A comprehensive guide to building a modern portfolio website using React for the frontend and Node.js with FastAPI for the backend, including MongoDB integration.",
            "cover_image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&h=600&fit=crop",
            "tags": ["React", "Node.js", "FastAPI", "MongoDB", "Portfolio"],
            "author": "Your Name",
            "published_date": "2026-03-07",
            "reading_time": "8 min read",
            "content": """Building a portfolio website is one of the best ways to showcase your skills and projects. In this article, I'll walk you through how I built my portfolio using modern web technologies.

## The Tech Stack

I chose React for the frontend because of its component-based architecture and excellent developer experience. For the backend, I went with Node.js and FastAPI (Python) to create a robust REST API. MongoDB serves as the database to store projects, blog posts, and contact information.

## Frontend Architecture

The React application is structured with clear separation of concerns:
- Components for reusable UI elements
- Services for API communication
- Styles organized by component
- Routing handled by React Router

This structure makes the codebase maintainable and scalable as the portfolio grows.

## Backend API Design

The FastAPI backend provides RESTful endpoints for:
- Project management (CRUD operations)
- Blog post management
- Contact form submissions
- Admin authentication

Each endpoint follows REST conventions and includes proper error handling and validation.

## Database Schema

MongoDB's flexible schema allows for easy updates. I store projects and blogs as separate collections, each with their own structure optimized for their use case.

## Deployment Considerations

When deploying, I ensured:
- Environment variables for sensitive data
- CORS configuration for API access
- Error handling for production
- Responsive design for all devices

## Lessons Learned

Building this portfolio taught me valuable lessons about full-stack development, API design, and deployment strategies. The experience reinforced the importance of clean code and proper architecture.

I hope this guide helps you build your own portfolio. Feel free to reach out if you have questions!""",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Building Scalable MERN Applications",
            "slug": "building-scalable-mern-applications",
            "short_description": "Best practices and patterns for building scalable applications using the MERN stack (MongoDB, Express, React, Node.js).",
            "cover_image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=600&fit=crop",
            "tags": ["MERN", "MongoDB", "Express", "React", "Node.js", "Architecture"],
            "author": "Your Name",
            "published_date": "2026-03-05",
            "reading_time": "10 min read",
            "content": """The MERN stack has become one of the most popular choices for building full-stack web applications. However, building scalable applications requires careful consideration of architecture, patterns, and best practices.

## Understanding Scalability

Scalability isn't just about handling more users. It's about:
- Performance optimization
- Code maintainability
- Database efficiency
- Deployment strategies

## Backend Architecture Patterns

### RESTful API Design

Designing a clean REST API is crucial. Use proper HTTP methods, status codes, and resource naming conventions. This makes your API intuitive and easy to consume.

### Database Optimization

MongoDB offers excellent flexibility, but requires careful indexing and query optimization. Use indexes for frequently queried fields and avoid N+1 query problems.

### Middleware and Error Handling

Implement comprehensive middleware for:
- Authentication and authorization
- Request validation
- Error handling
- Logging

## Frontend Best Practices

### Component Architecture

Organize React components logically:
- Container components for data fetching
- Presentational components for UI
- Shared components for reusability

### State Management

Choose the right state management solution:
- Local state for component-specific data
- Context API for shared state
- Redux for complex applications

### Performance Optimization

Implement:
- Code splitting
- Lazy loading
- Memoization
- Virtual scrolling for long lists

## Deployment and DevOps

### Environment Configuration

Use environment variables for:
- API endpoints
- Database connections
- Secret keys
- Feature flags

### CI/CD Pipeline

Automate:
- Testing
- Building
- Deployment
- Monitoring

## Conclusion

Building scalable MERN applications requires attention to detail at every level. Focus on clean architecture, proper patterns, and continuous optimization.""",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Best Practices for Structuring React Projects",
            "slug": "best-practices-for-structuring-react-projects",
            "short_description": "Learn how to organize your React projects for maintainability, scalability, and team collaboration.",
            "cover_image_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1200&h=600&fit=crop",
            "tags": ["React", "JavaScript", "Best Practices", "Architecture", "Code Organization"],
            "author": "Your Name",
            "published_date": "2026-03-03",
            "reading_time": "7 min read",
            "content": """A well-structured React project is the foundation of maintainable and scalable applications. In this article, I'll share best practices I've learned from building production React applications.

## Folder Structure

### Feature-Based Organization

Organize by features rather than file types:
```
src/
  components/
    Blog/
      Blog.jsx
      BlogList.jsx
      BlogDetail.jsx
      Blog.css
  services/
    api.js
  styles/
    App.css
```

This approach makes it easier to find related code and understand the application structure.

### Separation of Concerns

Keep components, services, and styles separate:
- Components handle UI and user interactions
- Services handle API calls and business logic
- Styles are co-located with components

## Component Design Principles

### Single Responsibility

Each component should have one clear purpose. If a component is doing too much, break it down into smaller components.

### Composition Over Inheritance

Use composition to build complex UIs from simple components. This makes components more reusable and testable.

### Props and State Management

- Use props for data that comes from parent components
- Use state for component-specific data
- Lift state up when multiple components need the same data

## Code Quality

### Naming Conventions

Use clear, descriptive names:
- Components: PascalCase (BlogCard)
- Functions: camelCase (fetchBlogs)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)

### File Organization

- One component per file
- Export default for main component
- Named exports for utilities

## Testing Strategy

### Component Testing

Test components in isolation:
- Render components with different props
- Test user interactions
- Verify expected behavior

### Integration Testing

Test how components work together:
- Test complete user flows
- Verify API integration
- Test routing

## Performance Considerations

### Code Splitting

Use React.lazy() and Suspense for route-based code splitting. This reduces initial bundle size and improves load times.

### Memoization

Use React.memo, useMemo, and useCallback appropriately to prevent unnecessary re-renders.

## Conclusion

Good project structure is an investment in your future self and your team. Take time to organize your code thoughtfully, and it will pay dividends as your project grows.""",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "How to Deploy Full Stack Applications",
            "slug": "how-to-deploy-full-stack-applications",
            "short_description": "A comprehensive guide to deploying React frontend and Node.js backend applications to production.",
            "cover_image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=600&fit=crop",
            "tags": ["Deployment", "DevOps", "React", "Node.js", "Production"],
            "author": "Your Name",
            "published_date": "2026-03-01",
            "reading_time": "9 min read",
            "content": """Deploying a full-stack application can be daunting, but with the right approach, it becomes straightforward. This guide covers everything you need to know about deploying React and Node.js applications.

## Pre-Deployment Checklist

Before deploying, ensure:
- All environment variables are configured
- Database connections are secure
- Error handling is comprehensive
- Logging is implemented
- Security best practices are followed

## Frontend Deployment

### Build Optimization

Create an optimized production build:
```bash
npm run build
```

This creates a minified, optimized bundle ready for production.

### Static Hosting Options

Popular options include:
- Vercel (excellent for React)
- Netlify
- AWS S3 + CloudFront
- GitHub Pages

### Environment Variables

Configure environment variables for:
- API endpoints
- Feature flags
- Analytics keys

## Backend Deployment

### Server Options

Choose based on your needs:
- Heroku (easy setup)
- AWS EC2 (more control)
- DigitalOcean (good balance)
- Railway (modern alternative)

### Process Management

Use PM2 or similar for:
- Process management
- Auto-restart on crashes
- Log management
- Load balancing

### Database Setup

Ensure your production database:
- Has proper backups
- Uses connection pooling
- Has monitoring enabled
- Follows security best practices

## CI/CD Pipeline

### Automated Testing

Run tests before deployment:
- Unit tests
- Integration tests
- E2E tests

### Automated Deployment

Set up:
- GitHub Actions
- GitLab CI
- CircleCI
- Or similar

## Monitoring and Maintenance

### Application Monitoring

Monitor:
- Error rates
- Response times
- Server resources
- Database performance

### Logging

Implement structured logging:
- Use appropriate log levels
- Include context
- Set up log aggregation

## Security Considerations

### HTTPS

Always use HTTPS in production. Most hosting providers offer free SSL certificates.

### Environment Variables

Never commit secrets. Use environment variables or secret management services.

### CORS Configuration

Configure CORS properly for your frontend domain.

## Conclusion

Deployment is a critical step in the development process. Take time to set it up correctly, and you'll have a reliable, scalable application in production.""",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Mastering JavaScript Async Patterns",
            "slug": "mastering-javascript-async-patterns",
            "short_description": "Deep dive into async/await, Promises, and modern asynchronous programming patterns in JavaScript.",
            "cover_image_url": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1200&h=600&fit=crop",
            "tags": ["JavaScript", "Async", "Promises", "Async/Await", "Programming"],
            "author": "Your Name",
            "published_date": "2026-02-28",
            "reading_time": "12 min read",
            "content": """Asynchronous programming is one of the most important concepts in modern JavaScript. Understanding how to work with async code effectively can make the difference between a smooth user experience and a frustrating one.

## Understanding Asynchronous JavaScript

JavaScript is single-threaded, which means it can only execute one thing at a time. However, with asynchronous programming, we can handle multiple operations without blocking the main thread.

## Callbacks: The Foundation

Callbacks were the original way to handle asynchronous operations in JavaScript. While they work, they can lead to callback hell when dealing with multiple nested operations.

## Promises: A Better Approach

Promises provide a cleaner way to handle asynchronous operations. They represent a value that may be available now, or in the future, or never.

### Creating Promises

You can create promises using the Promise constructor or using async functions that return promises.

### Chaining Promises

Promise chaining allows you to sequence asynchronous operations in a readable way. Each `.then()` returns a new promise, allowing you to chain operations.

## Async/Await: The Modern Solution

Async/await is syntactic sugar built on top of promises. It makes asynchronous code look and behave more like synchronous code.

### Error Handling

Use try/catch blocks with async/await for cleaner error handling compared to promise chains.

### Parallel Execution

Use `Promise.all()` to execute multiple async operations in parallel, or `Promise.allSettled()` if you want all promises to complete regardless of failures.

## Best Practices

1. Always handle errors properly
2. Use async/await for better readability
3. Avoid blocking the main thread
4. Use Promise.all() for parallel operations when possible
5. Consider using Promise.race() for timeout scenarios

## Common Pitfalls

- Forgetting to await promises
- Not handling errors properly
- Creating unnecessary promise chains
- Blocking the event loop

## Conclusion

Mastering async patterns in JavaScript is essential for building modern web applications. Start with promises, then move to async/await for cleaner, more maintainable code.""",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Database Design Principles for Web Applications",
            "slug": "database-design-principles-for-web-applications",
            "short_description": "Essential principles and best practices for designing efficient and scalable databases for web applications.",
            "cover_image_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=1200&h=600&fit=crop",
            "tags": ["Database", "MongoDB", "SQL", "Design", "Architecture"],
            "author": "Your Name",
            "published_date": "2026-02-25",
            "reading_time": "11 min read",
            "content": """Good database design is crucial for building performant and maintainable web applications. Whether you're using SQL or NoSQL databases, following sound design principles will save you time and headaches down the road.

## Understanding Your Data

Before designing your database, you need to understand:
- What data you need to store
- How data relates to each other
- How data will be accessed
- Expected data volume and growth

## Normalization vs Denormalization

### Normalization

Normalization reduces data redundancy and improves data integrity. It's essential for relational databases but can lead to complex queries.

### Denormalization

Denormalization improves read performance by reducing joins, but increases storage and complexity. It's common in NoSQL databases.

## Choosing the Right Database

### SQL Databases

Use SQL databases when:
- You need ACID transactions
- Data relationships are complex
- You need strong consistency

### NoSQL Databases

Use NoSQL databases when:
- You need horizontal scaling
- Schema is flexible
- You're dealing with large volumes of unstructured data

## Indexing Strategies

Proper indexing is crucial for performance:
- Index frequently queried fields
- Don't over-index (slows writes)
- Consider composite indexes for multi-field queries
- Monitor index usage and performance

## Data Modeling

### Relational Model

Design tables with proper relationships:
- One-to-one relationships
- One-to-many relationships
- Many-to-many relationships

### Document Model

Design documents based on access patterns:
- Embed related data that's accessed together
- Reference data that's accessed separately
- Consider document size limits

## Performance Optimization

1. Use appropriate data types
2. Implement proper indexing
3. Optimize queries
4. Use connection pooling
5. Implement caching strategies

## Security Considerations

- Always validate and sanitize input
- Use parameterized queries
- Implement proper access controls
- Encrypt sensitive data
- Regular backups

## Conclusion

Good database design requires balancing normalization, performance, and maintainability. Start with a solid foundation, and iterate based on your application's needs.""",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Building RESTful APIs with FastAPI",
            "slug": "building-restful-apis-with-fastapi",
            "short_description": "A practical guide to building modern, fast, and scalable REST APIs using Python's FastAPI framework.",
            "cover_image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&h=600&fit=crop",
            "tags": ["FastAPI", "Python", "REST API", "Backend", "Web Development"],
            "author": "Your Name",
            "published_date": "2026-02-22",
            "reading_time": "9 min read",
            "content": """FastAPI has quickly become one of the most popular Python web frameworks for building APIs. Its combination of speed, automatic documentation, and type hints makes it an excellent choice for modern web development.

## Why FastAPI?

FastAPI offers several advantages:
- High performance (comparable to Node.js and Go)
- Automatic API documentation
- Type hints and validation
- Easy to learn and use
- Built on modern Python standards

## Setting Up FastAPI

Getting started with FastAPI is straightforward. Install it using pip and create your first application.

## Routing and Endpoints

FastAPI uses decorators to define routes. You can create GET, POST, PUT, DELETE, and other HTTP method endpoints easily.

## Request and Response Models

Use Pydantic models to define request and response schemas. FastAPI automatically validates incoming data and generates documentation.

## Database Integration

FastAPI works well with various databases:
- SQL databases with SQLAlchemy
- NoSQL databases like MongoDB
- Async database drivers for better performance

## Authentication and Authorization

Implement security using:
- JWT tokens
- OAuth2
- API keys
- Custom authentication middleware

## Error Handling

FastAPI provides excellent error handling:
- HTTPException for custom errors
- Automatic validation errors
- Custom exception handlers

## Testing Your API

Test your FastAPI application using:
- pytest for unit tests
- TestClient for integration tests
- Automated testing in CI/CD

## Deployment

Deploy FastAPI applications using:
- Uvicorn or Gunicorn
- Docker containers
- Cloud platforms (AWS, Heroku, Railway)

## Best Practices

1. Use type hints everywhere
2. Leverage Pydantic for validation
3. Organize code with routers
4. Implement proper error handling
5. Write comprehensive tests
6. Document your API

## Conclusion

FastAPI makes building REST APIs in Python a joy. Its modern approach, excellent performance, and automatic documentation make it an ideal choice for any API project.""",
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    try:
        result = collection.insert_many(sample_blogs)
        print(f"[SUCCESS] Successfully inserted {len(result.inserted_ids)} sample blog(s)!")
        print("\nSample blogs created:")
        for blog in sample_blogs:
            print(f"  - {blog['title']} (slug: {blog['slug']})")
    except Exception as e:
        print(f"[ERROR] Failed to insert sample blogs: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting blog seed script...")
    seed_blogs()
    print("Seed script completed.")

