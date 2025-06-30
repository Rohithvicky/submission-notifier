import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from twilio.rest import Client

# Load from environment variables
USERNAME = os.getenv("ERP_USERNAME")
PASSWORD = os.getenv("ERP_PASSWORD")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = "whatsapp:+14155238886"  # Twilio Sandbox Number
YOUR_PHONE = os.getenv("YOUR_PHONE")     # Your verified WhatsApp number

def send_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(from_=TWILIO_PHONE, to=YOUR_PHONE, body=message)

def refresh_token():
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
    driver.get("https://erp.aurora.ac.in/login")

    # Log in to the ERP
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "submit").click()

    time.sleep(5)  # Wait for the page to load

    # Retrieve the token from the page (adjust the selector as needed)
    token = driver.execute_script("return localStorage.getItem('token');")

    driver.quit()
    return token

def check_submissions(token):
    url = f"https://aurorabackend.creatrixcampus.com/api/v1/examallocation/getstudentallocation/reqFor/ongoing/userid/{os.getenv('USER_ID')}"

    headers = {
        "token": token,
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
        for msg in alerts:
            send_alert(msg)
    else:
        send_alert("✅ Bot ran — no pending submissions found.")

# Main execution
token = refresh_token()
check_submissions(token)
