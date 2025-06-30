import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "your_username_here"
PASSWORD = "your_password_here"

def refresh_token():
    chrome_options = Options()
    # Run visible for debugging
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://erp.aurora.ac.in/auth/login")

    try:
        print("🔍 Current URL after load:", driver.current_url)
        wait = WebDriverWait(driver, 30)

        # Fill email
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="email"]'))
        )
        email_input.clear()
        email_input.send_keys(USERNAME)
        print("✅ Filled username")

        # Fill password
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)
        print("✅ Filled password")

        # Find and click button
        login_button = driver.find_element(By.ID, "kt_login_signin_submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)

        try:
            login_button.click()
            print("✅ Clicked login button")
        except ElementClickInterceptedException:
            print("⚠ Click intercepted, trying JS click")
            driver.execute_script("arguments[0].click();", login_button)

        # Wait a bit for login processing
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return !!localStorage.getItem('token');")
        )
        token = driver.execute_script("return localStorage.getItem('token');")
        print("✅ Token:", token)

        # Dump final page source for review
        with open("after_login.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ Saved after_login.html")

        input("⏸ Inspect browser and press Enter to close...")

    except Exception as e:
        print(f"❌ Login process failed: {e}")

    driver.quit()

refresh_token()
