from seleniumwire import webdriver
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
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://erp.aurora.ac.in/auth/login")

    try:
        print("🔍 Loaded:", driver.current_url)
        wait = WebDriverWait(driver, 30)

        # Fill username
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="email"]')))
        email_input.send_keys(USERNAME)

        # Fill password
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]')))
        password_input.send_keys(PASSWORD)

        # Click login
        login_button = driver.find_element(By.ID, "kt_login_signin_submit")
        login_button.click()

        # Wait for requests
        WebDriverWait(driver, 10).until(
            lambda d: any("aurorabackend.creatrixcampus.com" in r.url for r in driver.requests)
        )

        # Extract token
        for request in driver.requests:
            if "aurorabackend.creatrixcampus.com" in request.url and 'token' in request.headers:
                token = request.headers['token']
                print(f"✅ Token: {token}")
                with open("token.txt", "w", encoding="utf-8") as f:
                    f.write(token)
                break
        else:
            print("❌ Token not found in network requests.")

        input("⏸ Inspect browser, then press Enter to exit...")

    except Exception as e:
        print(f"❌ Error: {e}")

    driver.quit()

refresh_token()
