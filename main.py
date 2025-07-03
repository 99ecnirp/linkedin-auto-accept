from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from dotenv import load_dotenv
import time
import os

# Load environment variables
load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))

# Initialize Chrome WebDriver
def init_driver():
    print("in init driver")
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=linkedin_profile")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--remote-debugging-port=9222")

    if HEADLESS:
        chrome_options.add_argument("--headless=new")
        print("[+] Running in headless mode")

    driver_path = os.path.join(os.getcwd(), "chrome-win64", "chromedriver.exe")
    print("chromium path =>", driver_path)

    try:
        service = Service(executable_path=driver_path)
        print("after adding all arguments")
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print("Unexpected error in init driver:", e)
        return None

# Login only if needed
def login_if_needed(driver):
    print("in login")
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    current_url = driver.current_url

    if "login" in current_url:
        print("[+] Logging in...")
        driver.find_element(By.ID, "username").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(3)
    else:
        print("[+] Already logged in.")

# Click "Load more" repeatedly to load all invitations


def load_all_invitations(driver):
    print("[*] Clicking 'Load more' buttons to load all invites...")

    while True:
        try:
            load_more_button = driver.find_element(By.XPATH, '//button[.//span[text()="Load more"]]')
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)
            load_more_button.click()
            print("[+] Clicked 'Load more'")
            time.sleep(3)
        except StaleElementReferenceException:
            # DOM updated between finding and clicking, just retry
            print("[*] Stale element, retrying to find 'Load more' button...")
            time.sleep(2)
            continue
        except NoSuchElementException:
            print("[+] No more 'Load more' button found.")
            break
        except Exception as e:
            print("[+] Click failed or no more buttons:", e)
            break

    print("[+] All invitations loaded.")


# Retry wrapper for clicking a button

def click_with_retries(button, index, driver, xpath='//button[.//span[text()="Accept"]]'):
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            button.click()
            print(f"[{index}] Accepted on attempt {attempt}")
            return True
        except StaleElementReferenceException:
            print(f"[{index}] Stale element on attempt {attempt}, refetching button...")
            buttons = driver.find_elements(By.XPATH, xpath)
            if index - 1 < len(buttons):
                button = buttons[index - 1]
            time.sleep(1)
        except (ElementClickInterceptedException, NoSuchElementException) as e:
            print(f"[{index}] Retry {attempt} failed: {e}")
            time.sleep(1)
    print(f"[{index}] Failed after {RETRY_ATTEMPTS} attempts")
    return False


# Accept all invitations
def accept_all_invitations(driver):
    print("[*] Accepting connection requests...")
    buttons = driver.find_elements(By.XPATH, '//button[.//span[text()="Accept"]]')
    print(f"[+] Found {len(buttons)} invites.")

    for i, button in enumerate(buttons, start=1):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(0.5)
            click_with_retries(button, i, driver)
            time.sleep(1)
        except Exception as e:
            print(f"[{i}] Unexpected error: {e}")

# Main execution flow
def main():
    driver = init_driver()
    print("after init")

    if driver is None:
        print("Driver failed to start. Exiting...")
        return

    try:
        print("I am here")
        login_if_needed(driver)
        time.sleep(2)
        print("after login")

        driver.get("https://www.linkedin.com/mynetwork/invitation-manager/received/CONNECTION/")
        time.sleep(3)
        print("before loading all invitations")

        # Load all invitations by clicking "Load more"
        load_all_invitations(driver)

        # Accept all loaded invitations
        accept_all_invitations(driver)

    finally:
        driver.quit()
        print("Script complete.")

if __name__ == "__main__":
    main()
