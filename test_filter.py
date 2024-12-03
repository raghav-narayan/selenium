import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

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

def test_filter_by_green_label(driver):
    # Step 1: Open Trello login page and log in
    driver.get("https://trello.com/login")
    take_screenshot(driver, "trello_login_page")  # Screenshot after loading login page

    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys("rxr0654@mavs.uta.edu")  # Replace with your email
    email_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "email_entered")  # Screenshot after entering email

    # Wait for the password field to load, then input password
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("Luffy123!@#")  # Replace with your password
    password_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "password_entered")  # Screenshot after entering password

    # Verify successful login by waiting for the 'Boards' page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Boards')]"))
    )
    take_screenshot(driver, "logged_in")  # Screenshot after successful login

    # Step 2: Navigate to your Trello board
    driver.get("https://trello.com/b/GH3SE4Yw/my-trello-board")
    take_screenshot(driver, "navigated_to_board")  # Screenshot after navigating to board

    # Step 3: Click on the filter button using the new data-testid attribute
    filter_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='filter-popover-button']"))
    )
    filter_button.click()
    take_screenshot(driver, "filter_button_clicked")  # Screenshot after clicking filter button

    # Step 4: Select the green label in the dropdown for filtering
    green_label_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-color='green' and @data-testid='card-label']"))
    )
    green_label_filter.click()
    take_screenshot(driver, "green_label_selected")  # Screenshot after selecting green label

    # Step 5: Assert that filtering by the green label was successful
    filtered_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'color-blind-pattern-green')]"))
    )
    take_screenshot(driver, "filtered_cards_displayed")  # Screenshot after filtering

    # Ensure at least one card with the green label is displayed after filtering
    assert len(filtered_cards) > 0, "No cards with the green label found after filtering."

if __name__ == "__main__":
    pytest.main()
