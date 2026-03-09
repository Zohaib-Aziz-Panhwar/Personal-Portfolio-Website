"""
Email service for sending contact form notifications.
"""

import smtplib
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL


async def send_contact_notification(name: str, email: str, message: str, raise_on_error: bool = False):
    """
    Send an email notification when a contact form is submitted.
    
    Args:
        name: Contact person's name
        email: Contact person's email
        message: Contact message
        raise_on_error: If True, raise exceptions instead of silently failing
    """
    # Skip if email is not configured
    if not all([SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL]):
        error_msg = "Email not configured. Please add SMTP_USER, SMTP_PASSWORD, and RECIPIENT_EMAIL to your .env file"
        print(f"[WARNING] {error_msg}")
        print(f"[INFO] SMTP_USER: {'Set' if SMTP_USER else 'Not set'}, SMTP_PASSWORD: {'Set' if SMTP_PASSWORD else 'Not set'}, RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")
        if raise_on_error:
            raise ValueError(error_msg)
        return
    
    try:
        print(f"[INFO] Attempting to send email to {RECIPIENT_EMAIL}...")
        print(f"[INFO] Using SMTP server: {SMTP_HOST}:{SMTP_PORT}")
        print(f"[INFO] From: {SMTP_USER}")
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"New Contact Form Submission from {name}"
        
        # Create email body
        body = f"""
You have received a new contact form submission:

Name: {name}
Email: {email}
Message:
{message}

---
This is an automated message from your portfolio website.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using standard smtplib (more reliable than aiosmtplib)
        # Run in thread executor since smtplib is synchronous
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def send_email_sync():
            """Synchronous email sending function"""
            try:
                print(f"[INFO] Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}...")
                
                if SMTP_PORT == 465:
                    # Use SSL connection for port 465
                    print(f"[INFO] Using SSL connection (port 465)")
                    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                        print(f"[INFO] Connected to SMTP server with SSL")
                        server.login(SMTP_USER, SMTP_PASSWORD)
                        print(f"[INFO] Login successful")
                        server.send_message(msg)
                        print(f"[INFO] Message sent successfully")
                else:
                    # Use STARTTLS for port 587
                    print(f"[INFO] Using STARTTLS connection (port {SMTP_PORT})")
                    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                        print(f"[INFO] Connected to SMTP server")
                        server.ehlo()  # Identify ourselves to the server
                        if server.has_extn('STARTTLS'):
                            server.starttls()
                            server.ehlo()  # Re-identify after STARTTLS
                            print(f"[INFO] TLS started")
                        else:
                            print(f"[INFO] Warning: Server does not support STARTTLS")
                        server.login(SMTP_USER, SMTP_PASSWORD)
                        print(f"[INFO] Login successful")
                        server.send_message(msg)
                        print(f"[INFO] Message sent successfully")
                
                print(f"[SUCCESS] Email notification sent to {RECIPIENT_EMAIL}")
                return True
            except smtplib.SMTPAuthenticationError as e:
                error_msg = f"SMTP Authentication failed: {e}"
                print(f"[ERROR] {error_msg}")
                if raise_on_error:
                    raise Exception(error_msg) from e
                return False
            except smtplib.SMTPException as e:
                error_msg = f"SMTP Error: {e}"
                print(f"[ERROR] {error_msg}")
                if raise_on_error:
                    raise Exception(error_msg) from e
                return False
            except Exception as e:
                error_msg = f"Failed to send email: {e}"
                print(f"[ERROR] {error_msg}")
                if raise_on_error:
                    raise Exception(error_msg) from e
                return False
        
        # Run the synchronous email sending in a thread executor
        loop = asyncio.get_event_loop()
        email_executor = ThreadPoolExecutor(max_workers=1)
        result = await loop.run_in_executor(email_executor, send_email_sync)
        email_executor.shutdown(wait=False)
        
        return result
        
    except Exception as e:
        error_msg = f"Failed to send email notification: {e}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        if raise_on_error:
            raise Exception(error_msg) from e
        # Don't raise exception - email failure shouldn't break the contact form
        return False

