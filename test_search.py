import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Create a directory for screenshots if it doesn't exist
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, name):
    """Take a screenshot and save it to the screenshots directory."""
    filename = f"screenshots/{name}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot saved as {filename}")

def test_trello_login_and_search_navigation(driver):
    # Step 1: Open Trello login page and log in
    driver.get("https://trello.com/login")
    take_screenshot(driver, "trello_login_page")  # Screenshot after loading login page

    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys("rxr0654@mavs.uta.edu")
    email_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "email_entered")  # Screenshot after entering email

    # Wait for the password field to load, then input password
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("Luffy123!@#")
    password_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "password_entered")  # Screenshot after entering password

    # Verify successful login by waiting for the 'Boards' page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Boards')]"))
    )
    take_screenshot(driver, "logged_in")  # Screenshot after successful login

    # Step 2: Input "my trello" into the search bar
    search_bar = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )
    search_bar.send_keys("my trello")  # Input search text
    take_screenshot(driver, "search_inputted")  # Screenshot after inputting search text

    # Step 3: Wait for the dropdown to appear and select your board/workspace
    workspace_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='My Trello Board']"))
    )
    workspace_option.click()  # Click to navigate to the board
    take_screenshot(driver, "workspace_selected")  # Screenshot after selecting workspace

    # Step 4: Verify navigation to the board by checking that the URL contains the expected substring
    WebDriverWait(driver, 10).until(
        EC.url_contains("/b/GH3SE4Yw/")  # Adjust this part if your board URL is different
    )
    assert "/b/GH3SE4Yw/" in driver.current_url  # Verify that the URL contains the board's identifier
    take_screenshot(driver, "navigated_to_board")  # Screenshot after navigation

if __name__ == "__main__":
    pytest.main()
