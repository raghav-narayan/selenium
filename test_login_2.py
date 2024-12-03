import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Add a special flag to enable the "Chrome is being controlled by automation" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, step_name):
    # Create a directory for screenshots if it doesn't exist
    if not os.path.exists('screenshots_login'):
        os.makedirs('screenshots_login')
    # Save the screenshot
    screenshot_path = f'screenshots_login/{step_name}.png'
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def test_trello_login(driver):
    # Step 1: Open Trello login page and log in
    driver.get("https://trello.com/login")
    take_screenshot(driver, "open_login_page")

    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys("rxr0654@mavs.uta.edu")
    email_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "input_email")

    # Wait for the password field to load, then input password
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("Luffy123!@#")
    password_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "input_password")

    # Wait briefly to ensure the Chrome automation banner appears
    time.sleep(2)
    take_screenshot(driver, "chrome_controlled_by_automation")

    # Verify successful login by waiting for the 'Boards' element to load
    boards_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Boards')]"))
    )
    
    # Assert that the 'Boards' element is visible
    assert boards_element.is_displayed(), "Login failed or 'Boards' not visible after login."
    take_screenshot(driver, "login_successful")

if __name__ == "__main__":
    pytest.main()
