import os
import requests
from twilio.rest import Client

# Load from environment
TOKEN = os.getenv("MANUAL_ERP_TOKEN")
USER_ID = os.getenv("USER_ID")
SEMESTER = os.getenv("SEMESTER")
INSTITUTION = os.getenv("INSTITUTION")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
YOUR_PHONE = os.getenv("YOUR_PHONE")
TWILIO_PHONE = "whatsapp:+14155238886"  # Twilio sandbox

def send_alert(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        msg = client.messages.create(
            from_=TWILIO_PHONE,
            to=YOUR_PHONE,
            body=message
        )
        print(f"📤 Twilio message SID: {msg.sid}")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def check_submissions():
    url = f"https://aurorabackend.creatrixcampus.com/api/v1/examallocation/getstudentallocation/reqFor/ongoing/userid/{USER_ID}"
    headers = {
        "token": TOKEN,
        "semester": SEMESTER,
        "institution": INSTITUTION,
        "origin": "https://erp.aurora.ac.in",
        "referer": "https://erp.aurora.ac.in",
        "accept": "application/json, text/plain, */*",
    }

    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        send_alert(f"❌ API request failed: {e}")
        return

    if response.status_code == 401:
        send_alert("🔐 Token expired! Please update it in Railway env.")
        return

    if response.status_code != 200:
        send_alert(f"❌ API error: {response.status_code} {response.text}")
        return

    data = response.json()
    assignments = data.get("examallocation", [])
    pending = [
        f"📚 {a['name']} | {a['coursename']} | Due: {a['end_date']}"
        for a in assignments if a.get("assignment_status") == "Not Submitted"
    ]

    if pending:
        message = "📝 Pending Assignments:\n" + "\n".join(pending)
        send_alert(message)
    else:
        send_alert("✅ No pending submissions!")

if __name__ == "__main__":
    check_submissions()
