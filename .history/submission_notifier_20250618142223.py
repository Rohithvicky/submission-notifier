import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twilio.rest import Client
import time

# Load credentials from environment variables
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
YOUR_PHONE = os.getenv("YOUR_PHONE")
SMS_PHONE = os.getenv("SMS_PHONE")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def send_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(from_="whatsapp:" + TWILIO_PHONE, to=YOUR_PHONE, body=message)
    client.messages.create(from_=TWILIO_PHONE, to=SMS_PHONE, body=message)

def check_assignments():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://erp.aurora.ac.in/auth/login")
        time.sleep(5)

        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(10)

        # Stay on dashboard and search for assignment rows
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Not Submitted')]")
        alerts = []
        for button in buttons:
            row = button.find_element(By.XPATH, "./ancestor::tr")
            alerts.append("📚 Assignment Alert:
" + row.text.strip())

        if alerts:
            for msg in alerts:
                send_alert(msg)
        else:
            print("✅ No pending assignments found.")

    except Exception as e:
        send_alert("⚠️ Bot Error: " + str(e))

    finally:
        driver.quit()

check_assignments()