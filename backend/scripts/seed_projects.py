"""
Seed script to populate the database with sample case study projects.
Run this script to add sample projects to the database.
"""

import sys
import os
from datetime import datetime, timezone

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_projects_collection

def seed_projects():
    """Seed the database with sample case study projects."""
    collection = get_projects_collection()
    
    if collection is None:
        print("[ERROR] Cannot connect to database. Please check your MongoDB connection.")
        return
    
    # Check if projects already exist
    existing_count = collection.count_documents({})
    if existing_count > 0:
        print(f"[INFO] Database already contains {existing_count} project(s).")
        print("[INFO] Adding sample projects anyway to ensure we have enough for testing...")
    
    sample_projects = [
        {
            "title": "AI Resume Analyzer",
            "slug": "ai-resume-analyzer",
            "short_description": "An intelligent resume analysis system that uses NLP and machine learning to evaluate resumes, provide feedback, and match candidates with job requirements.",
            "detailed_description": "The AI Resume Analyzer is a comprehensive platform designed to revolutionize the recruitment process by leveraging cutting-edge natural language processing and machine learning technologies. This system addresses the critical challenges faced by both job seekers and recruiters in today's competitive job market.\n\nFor job seekers, the platform provides intelligent resume analysis that goes beyond simple keyword matching. It offers detailed feedback on resume structure, content quality, and ATS (Applicant Tracking System) compatibility. The system can identify missing skills, suggest improvements, and help candidates optimize their resumes for specific job descriptions.\n\nFor recruiters and HR professionals, the platform streamlines the hiring process by automatically parsing and analyzing resumes, extracting key information such as skills, experience levels, education, and certifications. It provides objective scoring and ranking of candidates, reducing bias and saving countless hours of manual review.\n\nThe system uses advanced NLP models trained on thousands of resumes and job descriptions to understand context, identify relevant skills, and match candidates to positions. It supports multiple resume formats including PDF, DOCX, and plain text, and can handle resumes in various layouts and structures.\n\nBuilt with scalability in mind, the platform can process hundreds of resumes simultaneously, providing real-time feedback and analysis. The microservices architecture ensures high availability and allows for independent scaling of different components based on demand.",
            "tech_stack": ["Python", "FastAPI", "React", "MongoDB", "TensorFlow", "NLTK", "Docker"],
            "tools": ["VS Code", "Postman", "Git", "Docker", "Jupyter Notebook", "MongoDB Compass"],
            "github_link": "https://github.com/example/ai-resume-analyzer",
            "live_demo": "https://ai-resume-analyzer.demo.com",
            "video_demo": "https://youtube.com/watch?v=example1",
            "problem_statement": "Recruiters and HR professionals spend countless hours manually reviewing resumes, which is time-consuming and prone to human bias. There's a need for an automated system that can quickly analyze resumes, extract key information, and provide objective feedback to help both job seekers improve their resumes and recruiters identify the best candidates efficiently.",
            "system_architecture": "The system follows a microservices architecture with three main components:\n\n1. **Frontend (React)**: User interface for uploading resumes and viewing analysis results. Built with React for component reusability and state management.\n\n2. **Backend API (FastAPI)**: RESTful API handling resume uploads, processing requests, and serving analysis results. Uses async operations for better performance.\n\n3. **ML Service (Python)**: Separate service running TensorFlow models for NLP processing, skill extraction, and resume scoring. Communicates with the API via message queue.\n\n4. **Database (MongoDB)**: Stores user data, resume metadata, and analysis results. Uses indexing for fast queries.\n\n5. **File Storage**: Cloud storage (S3-compatible) for storing uploaded resume PDFs and processed documents.\n\nThe architecture supports horizontal scaling and can handle multiple concurrent requests efficiently.",
            "key_features": [
                "Automated resume parsing and information extraction",
                "Skill matching against job descriptions",
                "Resume scoring with detailed feedback",
                "ATS (Applicant Tracking System) compatibility check",
                "Multi-format support (PDF, DOCX, TXT)",
                "Real-time analysis with progress tracking",
                "Export analysis reports in PDF format"
            ],
            "challenges": "1. **PDF Parsing Complexity**: Extracting text from various PDF formats while preserving structure was challenging. Different resume templates have varying layouts.\n\n2. **NLP Accuracy**: Training models to accurately identify skills, experience levels, and education details required extensive data preprocessing and model tuning.\n\n3. **Performance Optimization**: Processing large PDFs and running ML models needed optimization to provide results within acceptable time limits.\n\n4. **Data Privacy**: Ensuring sensitive resume data is handled securely and complies with data protection regulations.\n\n5. **Scalability**: Handling concurrent uploads and processing requests required implementing queue systems and load balancing.",
            "solutions": "1. **Hybrid Parsing Approach**: Combined multiple PDF parsing libraries (PyPDF2, pdfplumber) with custom logic to handle different formats. Implemented fallback mechanisms for edge cases.\n\n2. **Fine-tuned ML Models**: Used transfer learning with pre-trained BERT models, fine-tuned on resume-specific datasets. Implemented ensemble methods for better accuracy.\n\n3. **Async Processing**: Implemented asynchronous job queues using Celery for background processing. Used Redis for caching frequently accessed data.\n\n4. **Security Measures**: Implemented encryption at rest and in transit, role-based access control, and automatic data deletion after retention period.\n\n5. **Microservices Architecture**: Separated ML processing into independent services that can scale independently. Used Docker containers for easy deployment and scaling.",
            "future_improvements": "1. **Multi-language Support**: Extend NLP capabilities to support resumes in multiple languages.\n\n2. **Advanced Analytics Dashboard**: Build comprehensive analytics for recruiters showing trends, skill gaps, and market insights.\n\n3. **Integration with Job Boards**: Integrate with popular job boards (LinkedIn, Indeed) to automatically fetch and analyze job descriptions.\n\n4. **Real-time Collaboration**: Add features for recruiters to collaborate, share notes, and discuss candidates.\n\n5. **Mobile Application**: Develop mobile apps for iOS and Android to enable on-the-go resume analysis.\n\n6. **AI-powered Resume Builder**: Add a feature to help users build optimized resumes based on job descriptions.\n\n7. **Video Interview Analysis**: Extend capabilities to analyze video interviews using computer vision and speech recognition.",
            "cover_image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200&h=600&fit=crop",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Real-Time Chat Application",
            "slug": "real-time-chat-application",
            "short_description": "A scalable real-time messaging application with support for group chats, file sharing, and end-to-end encryption, built with modern web technologies.",
            "detailed_description": "The Real-Time Chat Application is a modern, scalable messaging platform designed to provide seamless communication experiences for teams and individuals. Built with performance and security as top priorities, this application delivers instant messaging capabilities that rival commercial solutions.\n\nThe application supports multiple communication modes including one-on-one private messaging, group chat rooms with customizable permissions, and broadcast channels for announcements. Each conversation type is optimized for its specific use case, ensuring smooth user experiences across all interaction patterns.\n\nSecurity is paramount in the design. The platform implements end-to-end encryption for private conversations, ensuring that only the intended recipients can read messages. User authentication is handled through JWT tokens, and all data transmission is secured using industry-standard encryption protocols.\n\nThe file sharing capabilities allow users to share images, documents, and media files directly within conversations. Files are stored securely in cloud storage, with automatic virus scanning and size limits to ensure system stability. The application provides progress indicators for file uploads and downloads, making it easy to track transfer status.\n\nReal-time features include typing indicators, read receipts, online/offline status, and message reactions. These features create a rich, engaging communication experience that keeps users connected and informed. The system uses WebSocket technology to ensure instant message delivery, with automatic reconnection handling for network interruptions.\n\nThe platform is designed to scale horizontally, capable of handling thousands of concurrent users across multiple server instances. Message history is stored efficiently in MongoDB with automatic cleanup of old messages, while Redis is used for caching and pub/sub messaging to ensure fast, reliable message distribution.",
            "tech_stack": ["Node.js", "Express", "Socket.io", "React", "MongoDB", "Redis", "JWT"],
            "tools": ["VS Code", "Postman", "Git", "Docker", "Redis CLI", "MongoDB Compass", "Chrome DevTools"],
            "github_link": "https://github.com/example/real-time-chat",
            "live_demo": "https://chat-app.demo.com",
            "video_demo": "https://youtube.com/watch?v=example2",
            "problem_statement": "Existing chat applications either lack real-time capabilities, have poor scalability, or compromise on security. There's a need for a modern chat solution that provides instant messaging, supports large groups, handles file sharing efficiently, and maintains user privacy through encryption, all while being able to scale to handle thousands of concurrent users.",
            "system_architecture": "The application uses a distributed architecture optimized for real-time communication:\n\n1. **Frontend (React)**: Single-page application with real-time updates using Socket.io client. Implements optimistic UI updates for better UX.\n\n2. **Backend API (Node.js/Express)**: RESTful API for user management, authentication, and message history. Uses JWT for stateless authentication.\n\n3. **WebSocket Server (Socket.io)**: Dedicated server handling real-time bidirectional communication. Supports rooms for group chats and private messaging.\n\n4. **Message Queue (Redis)**: Pub/Sub system for distributing messages across multiple server instances. Ensures message delivery even during server restarts.\n\n5. **Database (MongoDB)**: Stores user profiles, chat rooms, message history, and metadata. Uses TTL indexes for automatic cleanup of old messages.\n\n6. **File Storage**: Cloud storage for images, documents, and media files shared in chats.\n\n7. **Load Balancer**: Distributes WebSocket connections across multiple Socket.io servers for horizontal scaling.\n\nThe system is designed to handle 10,000+ concurrent connections per server instance.",
            "key_features": [
                "Real-time messaging with instant delivery",
                "Group chat rooms with admin controls",
                "Private one-on-one messaging",
                "File and image sharing",
                "End-to-end encryption for private chats",
                "Message read receipts and typing indicators",
                "User presence status (online/offline)",
                "Message search and history",
                "Push notifications for mobile",
                "Emoji reactions and message threads"
            ],
            "challenges": "1. **WebSocket Scalability**: Managing thousands of concurrent WebSocket connections and ensuring messages are delivered to all participants in group chats.\n\n2. **Message Ordering**: Ensuring messages appear in correct chronological order across different clients, especially with multiple server instances.\n\n3. **Real-time Synchronization**: Keeping all clients synchronized when users join/leave rooms or when messages are sent simultaneously.\n\n4. **Database Performance**: Handling high write loads from message storage while maintaining fast read performance for message history.\n\n5. **File Upload Handling**: Managing large file uploads without blocking the server or causing memory issues.\n\n6. **Cross-browser Compatibility**: Ensuring WebSocket connections work reliably across different browsers and handle reconnection gracefully.",
            "solutions": "1. **Redis Pub/Sub**: Implemented Redis pub/sub to distribute messages across multiple Socket.io server instances. Each server subscribes to relevant channels.\n\n2. **Message Sequencing**: Added timestamp-based sequencing and server-side message ordering. Implemented conflict resolution for edge cases.\n\n3. **Room Management**: Used Socket.io rooms for efficient message broadcasting. Implemented heartbeat mechanism to detect and handle disconnections.\n\n4. **Database Optimization**: Used MongoDB write concerns and indexing strategies. Implemented message batching for bulk inserts. Added read replicas for history queries.\n\n5. **Streaming Uploads**: Implemented chunked file uploads with progress tracking. Used cloud storage for direct client uploads to reduce server load.\n\n6. **Connection Management**: Implemented automatic reconnection logic with exponential backoff. Used Socket.io's built-in reconnection features and added custom fallback mechanisms.",
            "future_improvements": "1. **Video and Voice Calls**: Integrate WebRTC for peer-to-peer video and voice calling within the application.\n\n2. **Screen Sharing**: Add ability to share screens during group chats for collaboration.\n\n3. **Message Reactions and Threads**: Enhance group chats with threaded conversations and rich message reactions.\n\n4. **AI Chatbot Integration**: Add AI-powered chatbots for automated customer support or assistance.\n\n5. **Advanced Search**: Implement full-text search with filters for finding specific messages, files, or users.\n\n6. **Mobile Apps**: Develop native iOS and Android applications with push notifications.\n\n7. **Integration APIs**: Create APIs for third-party integrations (Slack, Teams, etc.).\n\n8. **Analytics Dashboard**: Build admin dashboard for monitoring usage, performance metrics, and user engagement.",
            "cover_image": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1200&h=600&fit=crop",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Smart Task Manager",
            "slug": "smart-task-manager",
            "short_description": "An intelligent task management system with AI-powered prioritization, automated scheduling, and team collaboration features.",
            "detailed_description": "The Smart Task Manager is an innovative productivity platform that combines artificial intelligence with intuitive task management to help individuals and teams work more efficiently. Unlike traditional task management tools that require manual organization, this system uses AI to automatically prioritize, schedule, and organize tasks based on deadlines, dependencies, and team capacity.\n\nThe core innovation lies in the AI-powered task analysis engine. When users create tasks, the system analyzes the description using natural language processing to extract key information such as deadlines, dependencies, priority levels, and required resources. This information is then used to automatically schedule tasks in an optimal sequence, taking into account team member availability and workload.\n\nThe platform offers multiple views to suit different working styles. The Kanban board provides a visual workflow with drag-and-drop functionality, allowing teams to see task progress at a glance. The calendar view shows tasks in a timeline format, making it easy to understand scheduling and deadlines. The list view offers detailed task information with filtering and sorting capabilities.\n\nTeam collaboration features include comments, mentions, file attachments, and activity feeds. Team members can be assigned to tasks, and the system automatically notifies relevant stakeholders when tasks are updated, completed, or when deadlines are approaching. The platform integrates with popular calendar applications like Google Calendar and Outlook, ensuring tasks are visible across all productivity tools.\n\nProductivity analytics provide valuable insights into team performance, workload distribution, and project progress. The system tracks time spent on tasks, identifies bottlenecks, and suggests optimizations. These insights help teams understand their work patterns and make data-driven decisions to improve efficiency.\n\nThe application is built with TypeScript for type safety, ensuring fewer bugs and better developer experience. The backend uses PostgreSQL for reliable data storage with Prisma ORM for type-safe database access. Real-time updates are delivered through WebSocket connections, ensuring all team members see changes instantly.",
            "tech_stack": ["React", "TypeScript", "Node.js", "PostgreSQL", "Prisma", "OpenAI API", "Docker"],
            "tools": ["VS Code", "Postman", "Git", "Docker", "pgAdmin", "Figma", "Jest"],
            "github_link": "https://github.com/example/smart-task-manager",
            "live_demo": "https://taskmanager.demo.com",
            "video_demo": "https://youtube.com/watch?v=example3",
            "problem_statement": "Traditional task management tools require manual prioritization and scheduling, which can be time-consuming and error-prone. Teams struggle with task overload, missed deadlines, and inefficient resource allocation. There's a need for an intelligent system that can automatically prioritize tasks based on deadlines, dependencies, and team capacity, while providing insights to help teams work more efficiently.",
            "system_architecture": "The system is built with a modern full-stack architecture:\n\n1. **Frontend (React + TypeScript)**: Type-safe React application with drag-and-drop task boards, calendar views, and real-time updates. Uses Context API for state management.\n\n2. **Backend API (Node.js)**: RESTful API with GraphQL endpoint for flexible data fetching. Implements rate limiting and caching for performance.\n\n3. **AI Service**: Integration with OpenAI API for intelligent task analysis, automatic categorization, and smart suggestions. Processes task descriptions to extract priorities and dependencies.\n\n4. **Database (PostgreSQL)**: Relational database storing users, projects, tasks, and relationships. Uses Prisma ORM for type-safe database access.\n\n5. **Task Scheduler**: Background service using cron jobs to automatically reschedule tasks, send reminders, and update priorities based on changing deadlines.\n\n6. **Notification Service**: Handles email and in-app notifications for task assignments, deadline reminders, and team updates.\n\n7. **Analytics Engine**: Processes task completion data to generate insights, productivity reports, and team performance metrics.\n\nThe architecture supports multi-tenancy with workspace isolation and role-based access control.",
            "key_features": [
                "AI-powered task prioritization",
                "Automated scheduling based on deadlines and dependencies",
                "Kanban boards with drag-and-drop",
                "Calendar view with timeline visualization",
                "Team collaboration with comments and mentions",
                "Task templates and recurring tasks",
                "Time tracking and productivity analytics",
                "Integration with calendar apps (Google Calendar, Outlook)",
                "Mobile-responsive design",
                "Real-time notifications and updates"
            ],
            "challenges": "1. **AI Integration Complexity**: Integrating AI for task analysis required careful prompt engineering and handling API rate limits and costs.\n\n2. **Dependency Management**: Building a system to automatically detect and manage task dependencies without creating circular references was complex.\n\n3. **Real-time Updates**: Ensuring all team members see task updates in real-time across different devices and browsers.\n\n4. **Performance with Large Datasets**: Handling thousands of tasks per workspace while maintaining fast load times and smooth interactions.\n\n5. **Conflict Resolution**: Managing concurrent edits to tasks and resolving conflicts when multiple users update the same task simultaneously.\n\n6. **Scheduling Algorithm**: Creating an algorithm that optimally schedules tasks considering dependencies, deadlines, and team member availability.",
            "solutions": "1. **Caching Strategy**: Implemented Redis caching for AI responses and frequently accessed data. Used prompt templates to reduce API calls.\n\n2. **Graph-based Dependency System**: Built a directed acyclic graph (DAG) to represent task dependencies. Implemented cycle detection and validation.\n\n3. **WebSocket Integration**: Used Socket.io for real-time updates. Implemented optimistic UI updates with conflict resolution on the backend.\n\n4. **Database Optimization**: Used PostgreSQL indexes, query optimization, and pagination. Implemented virtual scrolling for large task lists.\n\n5. **Operational Transform**: Implemented OT-like conflict resolution for concurrent edits. Used version numbers and last-write-wins for simple fields.\n\n6. **Constraint-based Scheduling**: Developed a constraint satisfaction algorithm that considers multiple factors (deadlines, dependencies, capacity) to generate optimal schedules. Used backtracking for complex scenarios.",
            "future_improvements": "1. **Machine Learning Models**: Train custom ML models on user behavior to improve task prioritization accuracy over time.\n\n2. **Natural Language Task Creation**: Allow users to create tasks using natural language (e.g., 'Schedule meeting with team next Friday').\n\n3. **Advanced Analytics**: Build predictive analytics to forecast project completion dates and identify potential bottlenecks.\n\n4. **Integration Marketplace**: Create integrations with popular tools (Slack, Jira, GitHub) for seamless workflow management.\n\n5. **Mobile Apps**: Develop native mobile applications for iOS and Android with offline support.\n\n6. **Automation Workflows**: Add visual workflow builder for creating custom automation rules and triggers.\n\n7. **Team Performance Insights**: Provide detailed analytics on team productivity, workload distribution, and capacity planning.\n\n8. **AI Assistant**: Build a conversational AI assistant that can help users manage tasks through natural language interactions.",
            "cover_image": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=1200&h=600&fit=crop",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "DevOps CI/CD Deployment Dashboard",
            "slug": "devops-cicd-deployment-dashboard",
            "short_description": "A comprehensive DevOps dashboard for monitoring CI/CD pipelines, deployment status, and infrastructure metrics with real-time updates and alerting.",
            "detailed_description": "The DevOps CI/CD Deployment Dashboard is a centralized monitoring and management platform designed to give DevOps teams complete visibility into their software delivery pipeline and infrastructure health. In modern software development, teams use multiple tools and platforms for CI/CD, container orchestration, and monitoring, making it challenging to get a unified view of system status.\n\nThis dashboard solves that problem by aggregating data from various sources including GitHub Actions, Jenkins, GitLab CI, Kubernetes clusters, Prometheus, and other monitoring tools. The platform provides a single pane of glass where teams can see the status of all their pipelines, recent deployments, infrastructure metrics, and alerts.\n\nThe real-time monitoring capabilities ensure that teams are immediately notified of pipeline failures, deployment issues, or infrastructure problems. The alerting system is highly configurable, allowing teams to set up custom notification rules based on specific conditions. Alerts can be sent via email, Slack, PagerDuty, or other notification channels.\n\nThe deployment tracking feature provides a complete history of all deployments across different environments. Teams can see what was deployed, when it was deployed, who deployed it, and the current status. The system supports rollback capabilities, allowing teams to quickly revert to previous versions if issues are detected.\n\nInfrastructure monitoring includes CPU usage, memory consumption, network traffic, and other key metrics. The dashboard displays these metrics in intuitive charts and graphs, making it easy to identify trends and potential issues. The system can handle data from hundreds of repositories and thousands of deployments, scaling horizontally to meet the needs of large organizations.\n\nThe customizable dashboard allows teams to create views tailored to their specific needs. Widgets can be added, removed, and rearranged to show the most relevant information. The platform also provides analytics on deployment frequency, success rates, and team activity, helping teams understand their delivery patterns and identify areas for improvement.",
            "tech_stack": ["Python", "FastAPI", "React", "Docker", "Kubernetes", "Prometheus", "Grafana", "GitHub Actions API"],
            "tools": ["VS Code", "Docker Desktop", "kubectl", "Helm", "Terraform", "Postman", "Git"],
            "github_link": "https://github.com/example/devops-dashboard",
            "live_demo": "https://devops-dashboard.demo.com",
            "video_demo": "https://youtube.com/watch?v=example4",
            "problem_statement": "DevOps teams struggle with visibility into their CI/CD pipelines, deployment status, and infrastructure health. Information is scattered across multiple tools (GitHub Actions, Jenkins, Kubernetes, etc.), making it difficult to get a unified view. There's a need for a centralized dashboard that aggregates data from various DevOps tools, provides real-time monitoring, and sends alerts when issues occur.",
            "system_architecture": "The dashboard follows a microservices architecture with data aggregation:\n\n1. **Frontend (React)**: Interactive dashboard with real-time charts, deployment timelines, and status indicators. Uses WebSockets for live updates.\n\n2. **Backend API (FastAPI)**: RESTful API aggregating data from multiple sources. Implements caching and rate limiting.\n\n3. **Data Collectors**: Multiple microservices that fetch data from:\n   - CI/CD platforms (GitHub Actions, Jenkins, GitLab CI)\n   - Container orchestration (Kubernetes, Docker Swarm)\n   - Monitoring tools (Prometheus, Datadog)\n   - Version control systems (GitHub, GitLab, Bitbucket)\n\n4. **Message Queue (RabbitMQ)**: Handles asynchronous data collection and processing. Ensures reliable data flow even during high load.\n\n5. **Time-Series Database (InfluxDB)**: Stores metrics, deployment history, and performance data. Optimized for time-based queries.\n\n6. **Alerting Service**: Monitors metrics and sends alerts via email, Slack, or PagerDuty when thresholds are exceeded.\n\n7. **Notification Service**: Handles real-time notifications to the frontend and external integrations.\n\nThe system is designed to handle data from hundreds of repositories and thousands of deployments.",
            "key_features": [
                "Unified view of all CI/CD pipelines",
                "Real-time deployment status tracking",
                "Infrastructure metrics and health monitoring",
                "Deployment history with rollback capabilities",
                "Customizable dashboards and widgets",
                "Alert management and notification rules",
                "Integration with major CI/CD platforms",
                "Kubernetes cluster monitoring",
                "Performance metrics and trends",
                "Team activity and deployment analytics"
            ],
            "challenges": "1. **Data Aggregation**: Collecting and normalizing data from multiple sources with different APIs, formats, and authentication methods.\n\n2. **Real-time Updates**: Providing real-time updates for hundreds of pipelines and deployments without overwhelming the frontend or backend.\n\n3. **Scalability**: Handling data from large organizations with thousands of repositories and frequent deployments.\n\n4. **Data Consistency**: Ensuring data consistency when collecting from multiple sources that may have different update frequencies.\n\n5. **API Rate Limits**: Managing API rate limits from various services (GitHub, GitLab, etc.) while maintaining up-to-date information.\n\n6. **Complex Queries**: Building efficient queries for time-series data and aggregating metrics across multiple dimensions.",
            "solutions": "1. **Adapter Pattern**: Created adapter services for each data source that normalize data into a common format. Implemented retry logic and error handling.\n\n2. **WebSocket with Room-based Updates**: Used Socket.io rooms to send updates only to relevant clients. Implemented data batching to reduce message frequency.\n\n3. **Horizontal Scaling**: Designed collectors as stateless services that can scale horizontally. Used load balancing and distributed caching.\n\n4. **Event Sourcing**: Implemented event sourcing for deployment data to maintain consistency. Used eventual consistency model for metrics.\n\n5. **Rate Limit Management**: Implemented token bucket algorithm for rate limiting. Used caching to reduce API calls. Implemented webhook subscriptions where available.\n\n6. **Time-Series Optimization**: Used InfluxDB with proper retention policies and downsampling. Implemented materialized views for common queries. Used Redis for frequently accessed aggregated data.",
            "future_improvements": "1. **Predictive Analytics**: Use ML models to predict deployment failures and infrastructure issues before they occur.\n\n2. **Automated Remediation**: Implement automated actions to fix common issues (auto-rollback, scaling, etc.) based on alerts.\n\n3. **Cost Optimization Insights**: Add cost tracking and recommendations for optimizing cloud infrastructure spending.\n\n4. **Security Scanning Integration**: Integrate security scanning tools to show vulnerabilities in deployments and dependencies.\n\n5. **Advanced Visualization**: Add 3D network topology views, dependency graphs, and interactive timeline visualizations.\n\n6. **Multi-cloud Support**: Extend support for AWS, Azure, and GCP with cloud-specific optimizations and integrations.\n\n7. **Collaboration Features**: Add team chat, deployment approvals, and collaborative incident management.\n\n8. **AI-powered Insights**: Use AI to analyze deployment patterns, identify bottlenecks, and suggest optimizations.",
            "cover_image": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=600&fit=crop",
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    try:
        result = collection.insert_many(sample_projects)
        print(f"[SUCCESS] Successfully inserted {len(result.inserted_ids)} sample project(s)!")
        print("\nSample projects created:")
        for project in sample_projects:
            print(f"  - {project['title']} (slug: {project['slug']})")
    except Exception as e:
        print(f"[ERROR] Failed to insert sample projects: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting project seed script...")
    seed_projects()
    print("Seed script completed.")

