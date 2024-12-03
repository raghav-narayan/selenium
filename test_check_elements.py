import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
import os

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, name):
    """Take a screenshot and save it to the specified directory."""
    screenshot_dir = "screenshots_check_elements"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

def safe_find_element(driver, by, value):
    """Safely find an element, retrying in case of StaleElementReferenceException."""
    for _ in range(3):  # Try three times
        try:
            return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, value)))
        except StaleElementReferenceException:
            pass  # Ignore the exception and retry
    take_screenshot(driver, f"element_not_found_{value}")  # Take a screenshot on failure
    raise Exception(f"Element with {by}='{value}' could not be found after retries.")

def test_trello_dashboard(driver):
    driver.get("https://trello.com/login")

    email_field = safe_find_element(driver, By.ID, 'username')
    email_field.send_keys("rxr0654@mavs.uta.edu")
    email_field.send_keys(Keys.ENTER)

    password_field = safe_find_element(driver, By.ID, "password")
    password_field.send_keys("Luffy123!@#")
    password_field.send_keys(Keys.ENTER)

    # Wait for the boards to load and check for visibility
    safe_find_element(driver, By.XPATH, "//span[contains(text(), 'Boards')]")

    driver.get("https://trello.com/b/GH3SE4Yw/my-trello-board")

    # 1. Verify "Add a card" button is present using data-testid
    add_card_button = safe_find_element(driver, By.CSS_SELECTOR, "button[data-testid='list-add-card-button']")
    assert add_card_button.is_displayed()

    # 2. Verify "Add another list" button is present
    add_list_button = safe_find_element(driver, By.XPATH, "//button[text()='Add another list']")
    assert add_list_button.is_displayed()

    # 3. Verify the search bar is present and can be interacted with
    search_bar = safe_find_element(driver, By.XPATH, "//input[@placeholder='Search']")
    search_bar.send_keys("test")  # Try searching for something
    assert search_bar.is_displayed()

if __name__ == "__main__":
    pytest.main()
