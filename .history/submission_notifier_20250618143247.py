import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
import time

# Twilio credentials
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

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"
    return webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

def check_assignments():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://erp.aurora.ac.in/auth/login")

        # Wait for login fields
        username_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@placeholder, 'Email') or contains(@name, 'email') or contains(@type, 'email')]")))
        password_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@type, 'password')]")))

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.submit()

        # Wait for dashboard
        time.sleep(10)

        # Find assignment rows
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Not Submitted')]")
        alerts = []

        for button in buttons:
            row = button.find_element(By.XPATH, "./ancestor::tr")
            alerts.append("📚 Assignment Alert:\n" + row.text.strip())

        if alerts:
            for msg in alerts:
                send_alert(msg)
        else:
            print("✅ No pending assignments found.")

    except Exception as e:
        print("Bot Error:", str(e))
        try:
            send_alert("⚠️ Submission Bot Error: " + str(e))
        except:
            print("❌ Failed to send alert.")

    finally:
        driver.quit()

check_assignments()
