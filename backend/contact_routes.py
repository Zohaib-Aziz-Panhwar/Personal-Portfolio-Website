"""
API routes for the FastAPI application.
"""

import asyncio
from fastapi import APIRouter
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from models import ContactRequest, ContactResponse
from database import get_contacts_collection
from email_service import send_contact_notification
from config import SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL

# Create router instance
router = APIRouter()

# Thread pool executor for running pymongo operations
executor = ThreadPoolExecutor(max_workers=5)


def save_to_mongodb(contact_data: dict):
    """
    Save contact data to MongoDB.
    Returns the inserted document ID as a string.
    """
    collection = get_contacts_collection()
    
    if collection is None:
        raise Exception("MongoDB is not configured or connection failed")
    
    # Insert document into MongoDB
    result = collection.insert_one(contact_data)
    
    # Convert ObjectId to string and return
    return str(result.inserted_id)


@router.post("/contact", response_model=ContactResponse)
async def submit_contact(request: ContactRequest) -> ContactResponse:
    """
    Submit a contact form message and save it to MongoDB.
    
    - **name**: Contact person's name (1-100 characters)
    - **email**: Valid email address
    - **message**: Contact message (10-1000 characters)
    
    Returns the submitted data with MongoDB-generated ID.
    """
    try:
        # Prepare document to save in MongoDB
        contact_document = {
            "name": request.name,
            "email": request.email,
            "message": request.message,
            "created_at": datetime.utcnow()
        }
        
        # Save to MongoDB using thread pool executor (since pymongo is synchronous)
        inserted_id = await asyncio.get_event_loop().run_in_executor(
            executor,
            save_to_mongodb,
            contact_document
        )
        
        # Send email in background so we can return the response immediately
        async def send_email_background():
            try:
                print(f"[INFO] Sending email notification for contact from {request.name} ({request.email})")
                email_result = await send_contact_notification(
                    name=request.name,
                    email=request.email,
                    message=request.message,
                    raise_on_error=False
                )
                if email_result:
                    print(f"[SUCCESS] Email notification sent for contact from {request.name}")
                else:
                    print(f"[WARNING] Email notification returned False for contact from {request.name}")
            except Exception as email_error:
                print(f"[ERROR] Email notification failed for contact from {request.name}: {email_error}")
        
        asyncio.create_task(send_email_background())
        
        # Return success response immediately (don't wait for email)
        response_data = {
            "id": inserted_id,
            "name": request.name,
            "email": request.email,
            "message": request.message
        }
        return ContactResponse(
            status="success",
            message="Message saved successfully",
            data=response_data
        )
    
    except Exception as e:
        # Log the error for debugging
        print(f"[ERROR] Failed to save contact: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error response if MongoDB save fails
        return ContactResponse(
            status="error",
            message="Failed to save message",
            data={}
        )


@router.get("/contact/test-email")
async def test_email_config():
    """
    Test endpoint to check email configuration and send a test email.
    """
    import smtplib
    from email.mime.text import MIMEText
    from config import SMTP_HOST, SMTP_PORT
    
    config_status = {
        "SMTP_USER": "Set" if SMTP_USER else "Not set",
        "SMTP_PASSWORD": "Set" if SMTP_PASSWORD else "Not set",
        "RECIPIENT_EMAIL": RECIPIENT_EMAIL,
        "SMTP_HOST": SMTP_HOST,
        "SMTP_PORT": SMTP_PORT,
        "all_configured": all([SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL])
    }
    
    if not config_status["all_configured"]:
        return {
            "status": "error",
            "message": "Email not fully configured. Please check your .env file.",
            "config": config_status
        }
    
    # Try using standard smtplib for more reliable error reporting
    try:
        print(f"[TEST] Attempting to send test email using smtplib...")
        print(f"[TEST] SMTP_HOST: {SMTP_HOST}, SMTP_PORT: {SMTP_PORT}")
        print(f"[TEST] SMTP_USER: {SMTP_USER}")
        print(f"[TEST] RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")
        
        # Create message
        msg = MIMEText("This is a test email to verify email configuration.")
        msg['From'] = SMTP_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Test Email from Portfolio API"
        
        # Send using standard smtplib
        # For Gmail, use port 587 with STARTTLS or port 465 with SSL
        if SMTP_PORT == 465:
            # Use SSL connection for port 465
            print(f"[TEST] Using SSL connection (port 465)")
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                print(f"[TEST] Connected to SMTP server with SSL")
                server.login(SMTP_USER, SMTP_PASSWORD)
                print(f"[TEST] Login successful")
                server.send_message(msg)
                print(f"[TEST] Message sent")
        else:
            # Use STARTTLS for port 587
            print(f"[TEST] Using STARTTLS connection (port {SMTP_PORT})")
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                print(f"[TEST] Connected to SMTP server")
                server.ehlo()  # Identify ourselves to the server
                if server.has_extn('STARTTLS'):
                    server.starttls()
                    server.ehlo()  # Re-identify after STARTTLS
                    print(f"[TEST] TLS started")
                else:
                    print(f"[TEST] Warning: Server does not support STARTTLS")
                server.login(SMTP_USER, SMTP_PASSWORD)
                print(f"[TEST] Login successful")
                server.send_message(msg)
                print(f"[TEST] Message sent")
        
        return {
            "status": "success",
            "message": "Test email sent successfully using smtplib! Check your inbox at panwerzohaib2@gmail.com",
            "config": config_status,
            "note": "If you don't see the email, check your spam folder. Also check server console for detailed logs."
        }
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication failed: {e}"
        print(f"[ERROR] {error_msg}")
        return {
            "status": "error",
            "message": error_msg,
            "config": config_status,
            "troubleshooting": {
                "issue": "Authentication failed",
                "solution": "Make sure you're using a Gmail App Password (16 characters), not your regular password",
                "steps": [
                    "1. Go to https://myaccount.google.com/apppasswords",
                    "2. Generate a new App Password for 'Mail'",
                    "3. Copy the 16-character password (remove spaces)",
                    "4. Update SMTP_PASSWORD in your .env file",
                    "5. Restart the server"
                ]
            }
        }
    except smtplib.SMTPException as e:
        error_msg = f"SMTP Error: {e}"
        print(f"[ERROR] {error_msg}")
        return {
            "status": "error",
            "message": error_msg,
            "config": config_status
        }
    except Exception as e:
        error_msg = f"Failed to send test email: {e}"
        print(f"[ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": error_msg,
            "config": config_status,
            "error_type": type(e).__name__
        }

