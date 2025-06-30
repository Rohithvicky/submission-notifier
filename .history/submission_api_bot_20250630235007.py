from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "vignesh.tokala@aurora.edu.in"
PASSWORD = "Rohith@123"

def refresh_token():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Keep visible for debug
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://erp.aurora.ac.in/auth/login")

    try:
        print("🔍 Current URL after load:", driver.current_url)
        wait = WebDriverWait(driver, 30)

        # Wait for username field
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="email"]'))
        )
        # No click — just send keys directly
        email_input.clear()
        email_input.send_keys(USERNAME)
        print("✅ Username filled")

        # Wait for password field
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)
        print("✅ Password filled")

        # Click login button
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "kt_login_signin_submit"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        login_button.click()
        print("✅ Clicked login button")

        # Wait for token
        wait.until(lambda d: d.execute_script("return !!localStorage.getItem('token');"))
        token = driver.execute_script("return localStorage.getItem('token');")
        print(f"✅ Token: {token}")

        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token or "No token found")

        input("⏸ Press Enter to close browser...")

    except Exception as e:
        print(f"❌ Login/token grab failed: {e}")

    driver.quit()

refresh_token()
