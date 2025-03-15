import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Use 'smtp-mail.outlook.com' for Outlook, etc.
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")



# URL to check
# URL = "https://www.portlandleathergoods.com/"
URL = "https://web.archive.org/web/20250129080104/https://www.portlandleathergoods.com/"

# Variations of "market tote" to search for
SEARCH_TERMS = [
    "market tote", "Market Tote", "MARKET TOTE",
    "Market-Tote", "market-tote", "MARKET-TOTE",
    "MarketTote", "markettote", "MARKETTOTE"
]

def send_email_alert(message):
    """Sends an email alert when Market Tote is found"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "Market Tote Back in Stock!"
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"🚨 Email failed: {e}")

def check_website():
    """Fetches the webpage and checks for keyword variations"""
    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")

        # Convert entire HTML to lowercase for easier matching
        page_text = soup.get_text().lower()

        for term in SEARCH_TERMS:
            if term.lower() in page_text:
                print(f"🛍️ Item found: {term}")
                send_email_alert(f"Market Tote is available! Check {URL}")
                return  # Stop checking after first match

        print("❌ Market Tote is NOT available.")

    except requests.RequestException as e:
        print(f"🚨 Error fetching the website: {e}")

if __name__ == "__main__":
    check_website()