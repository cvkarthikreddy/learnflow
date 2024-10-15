import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime

# SMTP2GO configuration
SMTP_SERVER = 'mail.smtp2go.com'
SMTP_PORT = 587  # Use 587 for TLS
USERNAME = 'DINESHS2235.SSE@SAVEETHA.COM'  # Replace with your SMTP2GO username
PASSWORD = 'KSSm4Fwb*fJ6X6Q'  # Replace with your SMTP2GO password

# Function to send email using SMTP2GO
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = to_address
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to schedule email
def schedule_email(to_address, subject, body, send_time):
    def job():
        send_email(to_address, subject, body)
    
    schedule.every().day.at(send_time).do(job)
    
    print(f"Scheduled email to be sent at {send_time}")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main function
def main():
    print("Automated Email Sender")
    
    to_address = input("Enter recipient's email address: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    
    send_time = input("Enter time to send the email (HH:MM, 24-hour format): ")
    
    # Validate time format
    try:
        datetime.strptime(send_time, '%H:%M')
    except ValueError:
        print("Invalid time format. Use HH:MM format.")
        return
    
    print(f"Scheduling email to be sent at {send_time}")
    schedule_email(to_address, subject, body, send_time)

if __name__ == "__main__":
    main()
