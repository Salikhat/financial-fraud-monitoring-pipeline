import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

def send_executive_report(
    excel_path="data/executive_risk_report.xlsx",
    sender_email="salikhat@gmail.com",
    sender_password="YOUR_APP_PASSWORD", # Secure Google App Password (not your normal password)
    recipient_email="stakeholder@example.com"
):
    print("📨 Initializing automated email dispatch sequence...")
    
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Could not locate report ledger at {excel_path}. Please execute the pipeline first.")

    # 1. Structure message containers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "📊 Automated Executive Risk & Fraud Monitoring Report"

    # 2. Compose professional email narrative body
    body = """Dear Executive Team,

Please find attached the automated data pipeline risk metrics ledger for today's processing cycle.

The report contains:
• Sheet 1: Core Financial KPI Summary Overview
• Sheet 2: Isolated Account Risk Exposure Profiles

This message was systematically compiled and dispatched via your local machine learning ingestion architecture.

Best Regards,
Data Pipeline Automation Engine
"""
    msg.attach(MIMEText(body, 'plain'))

    # 3. Read and encode the Excel file attachment asset
    print(f"📎 Packing attachment asset: {excel_path}")
    with open(excel_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(excel_path)}",
        )
        msg.attach(part)

    # 4. Connect to secure SMTP Server and transmit data
    try:
        print("🔐 Establishing connection to secure Gmail SMTP server line...")
        # Using Gmail's secure SMTP line on port 587
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls() # Secure encrypt connection channel
        
        print("🔑 Authenticating administrative delivery credentials...")
        server.login(sender_email, sender_password)
        
        print(f"🚀 Outbound transmitting package payload directly to: {recipient_email}")
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("✅ Executive risk alert report successfully emailed to stakeholders!\n")
        
    except Exception as e:
        print(f"❌ Failed to transmit email report due to security error: {e}")
        print("💡 Note: If using Gmail, ensure you have generated an 'App Password' from Google Account Settings.")

if __name__ == "__main__":
    # Substitute placeholder fields with your actual details to execute test transmissions
    send_executive_report()