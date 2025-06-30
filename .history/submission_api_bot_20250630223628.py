import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://erp.aurora.ac.in/auth/login")

    try:
        wait = WebDriverWait(driver, 30)

        # Wait for username input
        username_field = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[type='email']"))
        )
        username_field.clear()
        username_field.send_keys(USERNAME)

        # Wait for password input
        password_field = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_field.clear()
        password_field.send_keys(PASSWORD)

        # Wait for and click submit
        login_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], button[role='button']"))
        )
        login_btn.click()

        # Wait until token is available in localStorage
        wait.until(lambda d: d.execute_script("return !!localStorage.getItem('token');"))
        token = driver.execute_script("return localStorage.getItem('token');")

    except Exception as e:
        print("❌ Login or token retrieval failed:", e)
        token = None

    driver.quit()
    return token

def check_submissions(token):
    if not token:
        send_alert("❌ Bot could not retrieve token. Check login or page structure.")
        return

    url = f"https://aurorabackend.creatrixcampus.com/api/v1/examallocation/getstudentallocation/reqFor/ongoing/userid/{USER_ID}"

    headers = {
        "token": token,
        "semester": SEMESTER,
        "institution": INSTITUTION,
        "origin": "https://erp.aurora.ac.in",
        "referer": "https://erp.aurora.ac.in",
        "accept": "application/json, text/plain, */*",
    }

    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        send_alert(f"❌ API request failed: {str(e)}")
        return

    if response.status_code == 401:
        send_alert("🔐 Token expired or invalid! Please update credentials or check bot.")
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

# MAIN
token = refresh_token()
check_submissions(token)
