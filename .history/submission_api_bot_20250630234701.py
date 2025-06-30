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

        # Fill username
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="email"]'))
        )
        email_input.click()
        email_input.clear()
        for char in USERNAME:
            email_input.send_keys(char)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", email_input)

        # Fill password
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_input.click()
        password_input.clear()
        for char in PASSWORD:
            password_input.send_keys(char)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", password_input)

        # Click login
        login_button = driver.find_element(By.ID, "kt_login_signin_submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        login_button.click()
        print("✅ Clicked login button")

        # Wait for token to appear in localStorage
        wait.until(lambda d: d.execute_script("return !!localStorage.getItem('token');"))
        token = driver.execute_script("return localStorage.getItem('token');")
        print(f"✅ Token retrieved: {token}")

        # Save token to file
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token or "No token found")

        # Save page source
        with open("after_login.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        input("⏸ Login done. Inspect browser then press Enter to exit...")

    except Exception as e:
        print(f"❌ Login/token grab failed: {e}")

    driver.quit()

refresh_token()
