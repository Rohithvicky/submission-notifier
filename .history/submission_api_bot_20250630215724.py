import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from twilio.rest import Client

# Load environment variables
USERNAME = os.getenv("ERP_USERNAME")
PASSWORD = os.getenv("ERP_PASSWORD")
USER_ID = os.getenv("USER_ID")
SEMESTER = os.getenv("SEMESTER")
INSTITUTION = os.getenv("INSTITUTION")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = "whatsapp:+14155238886"  # Twilio Sandbox Number
YOUR_PHONE = os.getenv("YOUR_PHONE")     # Your verified WhatsApp number

def send_alert(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        msg = client.messages.create(
            from_=TWILIO_PHONE,
            to=YOUR_PHONE,
            body=message
        )
        print("📤 Twilio message SID:", msg.sid)
        print("📬 Message status:", msg.status)
    except Exception as e:
        print("❌ Failed to send WhatsApp alert:", str(e))

def refresh_token():
    driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH or set WebDriver path
    driver.get("https://erp.aurora.ac.in/login")

    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "submit").click()

    time.sleep(5)  # Adjust sleep as necessary

    token = driver.execute_script("return localStorage.getItem('token');")
    driver.quit()
    return token

def check_submissions(token):
    url = f"https://aurorabackend.creatrixcampus.com/api/v1/examallocation/getstudentallocation/reqFor/ongoing/userid/{USER_ID}"

    headers = {
        "token": token,
        "semester": SEMESTER,
        "institution": INSTITUTION,
        "origin": "https://erp.aurora.ac.in",
        "referer": "https://erp.aurora.ac.in",
        "accept": "application/json, text/plain, */*",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        send_alert("🔐 Token expired! Please update the TOKEN in Railway.")
        return

    if response.status_code != 200:
        send_alert(f"❌ API Error: {response.status_code} — {response.text}")
        return

    data = response.json()
    assignments = data.get("examallocation", [])
    alerts = []

    for a in assignments:
        if a.get("assignment_status") == "Not Submitted":
            alerts.append(f"📚 {a['name']}\n📘 {a['coursename']}\n🕒 Due: {a['end_date']}")

    if alerts:
        full_message = "📝 Pending Assignments:\n\n" + "\n\n".join(alerts)
        send_alert(full_message)
    else:
        send_alert("✅ Bot ran — no pending submissions found.")

# MAIN EXECUTION
token = refresh_token()
check_submissions(token)
