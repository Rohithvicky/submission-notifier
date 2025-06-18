import os
import requests
from twilio.rest import Client

# Load from Railway environment variables
TOKEN = os.getenv("TOKEN")
SEMESTER = os.getenv("SEMESTER")
INSTITUTION = os.getenv("INSTITUTION")
USER_ID = os.getenv("USER_ID")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = "whatsapp:+14155238886"  # Twilio Sandbox WhatsApp number
YOUR_PHONE = os.getenv("YOUR_PHONE")    # Your verified WhatsApp number

def send_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(
        from_=TWILIO_PHONE,
        to=YOUR_PHONE,
        body=message
    )

def check_submissions():
    url = f"https://aurorabackend.creatrixcampus.com/api/v1/examallocation/getstudentallocation/reqFor/ongoing/userid/{USER_ID}/sort[fieldname]/end_date/sort[order]/asc"

    headers = {
        "Token": TOKEN,
        "Semester": SEMESTER,
        "Institution": INSTITUTION,
        "Origin": "https://erp.aurora.ac.in",
        "Referer": "https://erp.aurora.ac.in",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        send_alert(f"❌ API Error: {response.status_code}")
        return

    data = response.json()
    assignments = data.get("examallocation", [])

    alerts = []
    for a in assignments:
        if a.get("assignment_status") == "Not Submitted":
            alerts.append(
                f"📚 {a['name']}\n📘 {a['coursename']}\n🕒 Due: {a['end_date']}"
            )

    if alerts:
        for msg in alerts:
            send_alert(msg)
    else:
        send_alert("✅ Bot ran — no pending submissions found.")

check_submissions()
