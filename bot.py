import os
import smtplib
from datetime import date
from email.mime.text import MIMEText
import requests


# -- FUNCTION 1: Weather ----------------------------------------------------
def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing whitespace/newlines
    except Exception as e:
        return f"Weather unavailable ({e})"


# -- FUNCTION 2: Quote ------------------------------------------------------
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()  # converts JSON text to a Python List
        quote = data[0]["q"]  # the quote text
        author = data[0]["a"]  # the author name
        return f'"{quote}" - {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"


# -- FUNCTION 3: Email Delivery (Advanced Extension) -----------------------
def send_email(summary_text):
    """Send the generated daily summary via email using safe GitHub Secrets."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    # If any secret is missing, print a warning to the logs and exit cleanly
    if not sender or not password or not receiver:
        print(
            "⚠️ Email configuration missing. Skipping email delivery step."
        )
        print("Ensure EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECEIVER secrets are added.")
        return

    # Construct the email payload
    msg = MIMEText(summary_text)
    msg["Subject"] = "Pulse - Daily Summary"
    msg["From"] = sender
    msg["To"] = receiver

    # Connect to Google's SMTP server and dispatch the email securely
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# -- FUNCTION 4: Build the summary -----------------------------------------
def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime("%A, %d %B %Y")  # e.g. Monday, 09 June 2026
    weather = get_weather()
    quote = get_quote()

    # Triple-quoted strings span multiple lines - great for formatted output
    summary = f"""=====================================
PULSE - Daily Summary
{today}
=====================================

WEATHER
{weather}

TODAY'S QUOTE
{quote}

====================================="""

    return summary


# -- FUNCTION 5: Run everything --------------------------------------------
def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()

    # 1. Print to the GitHub Actions Log
    print(summary)

    # 2. Save to a file (for the downloadable artifact workflow)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    # 3. Fire the summary straight to your inbox!
    send_email(summary)

    print("Pulse ran successfully.")


# -- Entry point guard ------------------------------------------------------
if __name__ == "__main__":
    run()