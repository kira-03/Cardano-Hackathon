"""
Email Service - Send emails with PDF attachments
Supports Gmail, Outlook, and custom SMTP
"""
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional
import os
from datetime import datetime
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)


class EmailService:
    """Professional email sending service with retry logic
    
    For Gmail:
    1. Enable 2-Factor Authentication on your Google account
    2. Go to https://myaccount.google.com/apppasswords
    3. Generate an App Password for 'Mail'
    4. Set environment variables:
       - SMTP_USER=your.email@gmail.com
       - SMTP_PASSWORD=your-16-char-app-password
    """
    
    def __init__(self):
        # Force reload environment variables
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        # Load from environment variables with defaults
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "").strip()
        # Remove any spaces from password (common copy-paste issue)
        self.smtp_password = os.getenv("SMTP_PASSWORD", "").strip().replace(" ", "")
        self.sender_email = os.getenv("SENDER_EMAIL", self.smtp_user)
        self.sender_name = os.getenv("SENDER_NAME", "Cross-Chain Navigator")
        self.reply_to = os.getenv("REPLY_TO_EMAIL", self.sender_email)
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 3  # seconds (increased for Gmail rate limits)
        
        # Email delivery log
        self.delivery_log = []
        
        # Log configuration status
        if self.smtp_user and self.smtp_password:
            masked_pwd = f"{self.smtp_password[:4]}...{self.smtp_password[-4:]}" if len(self.smtp_password) > 8 else "****"
            logger.info(f"✅ Email service configured with {self.smtp_host}:{self.smtp_port}")
            logger.info(f"   Sender: {self.sender_email}")
            logger.info(f"   Password length: {len(self.smtp_password)} chars (should be 16 for Gmail App Password)")
            logger.info(f"   Password preview: {masked_pwd}")
        else:
            logger.warning("⚠️ Email service not configured - set SMTP_USER and SMTP_PASSWORD")
    
    def _validate_email(self, email: str) -> bool:
        """Basic email validation"""
        return "@" in email and "." in email.split("@")[1]
    
    def _log_delivery(self, status: str, recipient: str, subject: str, error: Optional[str] = None):
        """Log email delivery attempt"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,  # success, failed, retrying
            "recipient": recipient,
            "subject": subject,
            "error": error
        }
        self.delivery_log.append(log_entry)
        logger.info(f"Email delivery log: {log_entry}")
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        body_text: str,
        attachments: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send email with PDF attachments and retry logic
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body_html: HTML formatted email body
            body_text: Plain text email body (fallback)
            attachments: List of file paths to attach
            cc: List of CC email addresses
            bcc: List of BCC email addresses
            reply_to: Custom reply-to address
            
        Returns:
            Dict with status and message
        """
        # Validate configuration
        if not self.smtp_user or not self.smtp_password:
            logger.warning("Email credentials not configured - email sending disabled")
            logger.info("""To enable email:
            1. For Gmail: Enable 2FA, then create App Password at https://myaccount.google.com/apppasswords
            2. Set environment variables:
               SMTP_USER=your.email@gmail.com
               SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx (16-char app password)
            """)
            return {
                "success": False,
                "message": "Email not configured. Set SMTP_USER and SMTP_PASSWORD environment variables. For Gmail, use an App Password (not your regular password).",
                "mock": True
            }
        
        # Validate recipient
        if not self._validate_email(to_email):
            error_msg = f"Invalid recipient email: {to_email}"
            logger.error(error_msg)
            self._log_delivery("failed", to_email, subject, error_msg)
            return {"success": False, "message": error_msg}
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Reply-To'] = reply_to or self.reply_to
        
        # Add CC and BCC
        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)
        
        # Attach plain text and HTML versions
        msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))
        
        # Attach files
        if attachments:
            for filepath in attachments:
                if not os.path.exists(filepath):
                    logger.warning(f"Attachment not found: {filepath}")
                    continue
                
                try:
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        filename = Path(filepath).name
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {filename}'
                        )
                        msg.attach(part)
                except Exception as e:
                    logger.error(f"Error attaching file {filepath}: {e}")
        
        # Send with retry logic
        for attempt in range(self.max_retries):
            server = None
            try:
                logger.info(f"📧 Attempt {attempt + 1}/{self.max_retries}: Connecting to {self.smtp_host}:{self.smtp_port}")
                
                # For Gmail, use SSL (port 465) which is more reliable
                # If port 587 is configured, try to switch to 465 for better compatibility
                try:
                    if self.smtp_port == 465:
                        # Direct SSL connection
                        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=15)
                        logger.info(f"✓ Connected via SSL on port {self.smtp_port}")
                    else:
                        # Try STARTTLS on port 587
                        server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15)
                        server.set_debuglevel(0)
                        server.ehlo()
                        if server.has_extn('STARTTLS'):
                            server.starttls()
                            server.ehlo()
                            logger.info(f"✓ Connected via STARTTLS on port {self.smtp_port}")
                        else:
                            # Fallback: Try SSL on port 465 if STARTTLS not supported
                            server.quit()
                            logger.warning(f"STARTTLS not available on port {self.smtp_port}, trying SSL on 465")
                            server = smtplib.SMTP_SSL(self.smtp_host, 465, timeout=15)
                            logger.info(f"✓ Connected via SSL on port 465 (fallback)")
                except Exception as conn_err:
                    logger.error(f"Connection error: {conn_err}")
                    raise
                
                logger.info(f"🔐 Authenticating as {self.smtp_user}")
                try:
                    server.login(self.smtp_user, self.smtp_password)
                    logger.info(f"✅ Authentication successful")
                except smtplib.SMTPAuthenticationError as auth_err:
                    logger.error(f"❌ Authentication failed: {auth_err}")
                    raise
                
                # Send email
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                logger.info(f"📤 Sending email to {len(recipients)} recipient(s)")
                server.sendmail(self.sender_email, recipients, msg.as_string())
                server.quit()
                
                # Success
                self._log_delivery("success", to_email, subject)
                logger.info(f"✅ Email sent successfully to {to_email}")
                return {
                    "success": True,
                    "message": f"Email sent to {to_email}",
                    "recipient": to_email,
                    "subject": subject,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except smtplib.SMTPAuthenticationError as e:
                error_msg = f"Authentication rejected by Gmail: {str(e)}. Possible causes: 1) Invalid App Password, 2) 2FA not enabled, 3) Gmail blocking login"
                logger.error(error_msg)
                self._log_delivery("failed", to_email, subject, error_msg)
                if server:
                    try:
                        server.quit()
                    except:
                        pass
                return {
                    "success": False,
                    "message": f"Gmail rejected login. Steps to fix: 1) Verify 2FA is ON at https://myaccount.google.com/security, 2) Delete old App Password and create NEW one at https://myaccount.google.com/apppasswords, 3) Update .env with new password. Error: {str(e)}",
                    "error": str(e)
                }
                
            except smtplib.SMTPException as e:
                error_msg = f"SMTP error on attempt {attempt + 1}: {e}"
                logger.warning(error_msg)
                
                if server:
                    try:
                        server.quit()
                    except:
                        pass
                
                if attempt < self.max_retries - 1:
                    self._log_delivery("retrying", to_email, subject, error_msg)
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    self._log_delivery("failed", to_email, subject, error_msg)
                    return {
                        "success": False,
                        "message": f"Failed to send email after {self.max_retries} attempts. Gmail may be blocking the connection. Try: 1) Generate new App Password, 2) Check https://myaccount.google.com/lesssecureapps",
                        "error": str(e)
                    }
                    
            except Exception as e:
                error_msg = f"Unexpected error: {e}"
                logger.error(error_msg, exc_info=True)
                self._log_delivery("failed", to_email, subject, error_msg)
                
                if server:
                    try:
                        server.quit()
                    except:
                        pass
                
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    return {
                        "success": False,
                        "message": "An unexpected error occurred while sending email",
                        "error": str(e)
                    }
        
        # Should not reach here
        return {
            "success": False,
            "message": "Failed to send email after all retries"
        }
    
    async def send_analysis_report(
        self,
        to_email: str,
        token_name: str,
        token_symbol: str,
        pdf_path: str,
        readiness_score: float,
        grade: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Send token analysis report via email
        
        Convenience method with pre-formatted template
        """
        subject = f"Token Readiness Report — {token_name} ({token_symbol})"
        
        # HTML email body with branding
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .header .token {{
            font-size: 18px;
            opacity: 0.9;
            margin-top: 8px;
        }}
        .content {{
            background: #ffffff;
            padding: 30px;
            border: 1px solid #e2e8f0;
            border-top: none;
        }}
        .score-box {{
            background: #f1f5f9;
            border-left: 4px solid #3B82F6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .score-box .grade {{
            font-size: 48px;
            font-weight: bold;
            color: #3B82F6;
            margin: 0;
        }}
        .score-box .score {{
            font-size: 20px;
            color: #64748b;
            margin: 5px 0 0 0;
        }}
        .button {{
            display: inline-block;
            background: #3B82F6;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            margin: 15px 0;
        }}
        .footer {{
            background: #f8fafc;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
            border-radius: 0 0 8px 8px;
            border: 1px solid #e2e8f0;
            border-top: none;
        }}
        .feature-list {{
            list-style: none;
            padding: 0;
        }}
        .feature-list li {{
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        .feature-list li:last-child {{
            border-bottom: none;
        }}
        .checkmark {{
            color: #10b981;
            font-weight: bold;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Token Analysis Report</h1>
        <div class="token">{token_name} ({token_symbol})</div>
    </div>
    
    <div class="content">
        <p>Dear Token Team,</p>
        
        <p>Your comprehensive token analysis report is ready! We've analyzed your token's readiness for exchange listings using our AI-powered EcosystemBridge Assistant.</p>
        
        <div class="score-box">
            <p class="grade">{grade}</p>
            <p class="score">Overall Readiness Score: {readiness_score:.0f}/100</p>
        </div>
        
        <h3>📊 Your Report Includes:</h3>
        <ul class="feature-list">
            <li><span class="checkmark">✓</span> Executive Summary & Key Insights</li>
            <li><span class="checkmark">✓</span> Detailed Token Metrics Analysis</li>
            <li><span class="checkmark">✓</span> Holder Distribution Breakdown</li>
            <li><span class="checkmark">✓</span> Exchange Requirements Assessment</li>
            <li><span class="checkmark">✓</span> Prioritized Improvement Recommendations</li>
            <li><span class="checkmark">✓</span> Cross-Chain Bridge Routes Analysis</li>
            <li><span class="checkmark">✓</span> Actionable Next Steps</li>
        </ul>
        
        <p style="margin-top: 25px;">
            <strong>📎 The complete PDF report is attached to this email.</strong>
        </p>
        
        <p>If you have any questions about the analysis or need guidance on implementing the recommendations, please don't hesitate to reach out.</p>
        
        <p>Best regards,<br>
        <strong>Cross-Chain Navigator Team</strong></p>
    </div>
    
    <div class="footer">
        <p>This report was generated by Cross-Chain Navigator's AI-powered analysis engine.</p>
        <p>Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}</p>
        <p style="margin-top: 10px; font-size: 11px; opacity: 0.7;">
            This report is for informational purposes only and does not constitute financial advice.
        </p>
    </div>
</body>
</html>
"""
        
        # Plain text version
        body_text = f"""
Token Analysis Report - {token_name} ({token_symbol})

Dear Token Team,

Your comprehensive token analysis report is ready!

Overall Readiness Score: {readiness_score:.0f}/100 (Grade: {grade})

Your Report Includes:
✓ Executive Summary & Key Insights
✓ Detailed Token Metrics Analysis
✓ Holder Distribution Breakdown
✓ Exchange Requirements Assessment
✓ Prioritized Improvement Recommendations
✓ Cross-Chain Bridge Routes Analysis
✓ Actionable Next Steps

The complete PDF report is attached to this email.

If you have any questions, please don't hesitate to reach out.

Best regards,
Cross-Chain Navigator Team

---
Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}
This report is for informational purposes only.
"""
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            attachments=[pdf_path] if pdf_path and os.path.exists(pdf_path) else [],
            cc=cc
        )
    
    def get_delivery_log(self, limit: int = 50) -> List[Dict]:
        """Get recent email delivery log"""
        return self.delivery_log[-limit:]
    
    def clear_delivery_log(self):
        """Clear delivery log"""
        self.delivery_log = []
        logger.info("Email delivery log cleared")
