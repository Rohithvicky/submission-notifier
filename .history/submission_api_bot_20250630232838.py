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
    # chrome_options.add_argument("--headless")  # Keep visible for testing
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://erp.aurora.ac.in/auth/login")

    try:
        print("🔍 Current URL after load:", driver.current_url)
        wait = WebDriverWait(driver, 30)

        # Enter username
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="email"]'))
        )
        email_input.click()
        email_input.clear()
        for char in USERNAME:
            email_input.send_keys(char)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", email_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", email_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('blur'));", email_input)
        print("✅ Entered username")

        # Enter password
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_input.click()
        password_input.clear()
        for char in PASSWORD:
            password_input.send_keys(char)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", password_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", password_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('blur'));", password_input)
        print("✅ Entered password")

        # Click login button
        login_button = driver.find_element(By.ID, "kt_login_signin_submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        login_button.click()
        print("✅ Clicked login button")

        # Try to grab token
        wait.until(lambda d: d.execute_script("return !!localStorage.getItem('token');"))
        token = driver.execute_script("return localStorage.getItem('token');")
        print("✅ Token retrieved:", token)

        # Save page source for debug
        with open("after_login.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ Saved after_login.html")

        input("⏸ Press Enter after inspecting browser to close...")

    except Exception as e:
        print(f"❌ Login process failed: {e}")

    driver.quit()

refresh_token()
