import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, step_name):
    # Create a directory for screenshots if it doesn't exist
    if not os.path.exists('screenshots_invalid'):
        os.makedirs('screenshots_invalid')
    # Save the screenshot
    screenshot_path = f'screenshots_invalid/{step_name}.png'
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def test_invalid_password_login(driver):
    # Open Trello login page
    driver.get("https://trello.com/login")
    take_screenshot(driver, "open_login_page")

    # Input correct email and submit
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys("rxr0654@mavs.uta.edu")  # Correct email ID
    email_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "input_email")

    # Wait for the password field to load, then input an incorrect password
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("WrongPassword123!")  # Incorrect password
    password_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "input_password")

    # Verify error message appears for incorrect password using the exact XPath provided
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='WhiteboxContainer']/section/div[2]/div/section/div/div[2]/span"))
    )
    take_screenshot(driver, "error_message_displayed")

    assert "Incorrect email address and / or password. If you recently migrated your Trello account to an Atlassian account, you will need to use your Atlassian account password" in error_message.text, "Error message not displayed for invalid credentials"

if __name__ == "__main__":
    pytest.main()
