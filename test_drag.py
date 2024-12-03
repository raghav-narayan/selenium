import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import os

# Create a directory for screenshots if it doesn't exist
screenshot_dir = 'screenshots_drag'
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def safe_find_element(driver, by, value):
    """Safely find an element, retrying in case of StaleElementReferenceException."""
    for _ in range(3):  # Try three times
        try:
            return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, value)))
        except StaleElementReferenceException:
            pass  # Ignore the exception and retry
    raise Exception(f"Element with {by}='{value}' could not be found after retries.")

def take_screenshot(driver, name):
    """Take a screenshot and save it to the screenshots directory."""
    filename = f"{screenshot_dir}/{name}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot saved as {filename}")

def test_drag_and_drop_card(driver):
    # Navigate to Trello login page
    driver.get("https://trello.com/login")

    # Log in to Trello
    email_field = safe_find_element(driver, By.ID, 'username')
    email_field.send_keys("rxr0654@mavs.uta.edu")  # Replace with your email
    email_field.send_keys(Keys.ENTER)

    password_field = safe_find_element(driver, By.ID, "password")
    password_field.send_keys("Luffy123!@#")  # Replace with your password
    password_field.send_keys(Keys.ENTER)

    # Wait for the dashboard to load
    safe_find_element(driver, By.XPATH, "//span[contains(text(), 'Boards')]")

    # Navigate to your Trello board
    driver.get("https://trello.com/b/GH3SE4Yw/my-trello-board")

    # Wait for lists to be present using data-testid attribute
    lists = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="list"]'))
    )

    # Check if lists are present
    if lists:
        print(f'Lists are present: {len(lists)} found.')
    else:
        print('No lists are present.')

    # Locate the source card (to be dragged)
    try:
        card_to_drag = safe_find_element(driver, By.XPATH, "//a[contains(text(), 'Design and development')]")  # Replace 'Card Title' with the actual title of the card
    except Exception as e:
        take_screenshot(driver, "card_drag_failure")
        raise e

    # Use the already selected lists to locate the target list (the second list)
    if len(lists) > 1:  # Ensure there are at least two lists
        target_list = lists[1]  # Select the second list
    else:
        take_screenshot(driver, "insufficient_lists")
        raise Exception("Not enough lists found to perform the drag-and-drop operation.")

    # Take a screenshot before performing the drag-and-drop action
    take_screenshot(driver, "before_drag_and_drop")  # Screenshot before drag-and-drop

    # Perform drag-and-drop
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(card_to_drag).move_to_element(target_list).release().perform()

    # Verify the card is now in the target list
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Design and development')]"))  # Replace 'Card Title' with the actual title of the card
        )
        take_screenshot(driver, "drag_and_drop_success")  # Screenshot after successful drag-and-drop
    except Exception as e:
        take_screenshot(driver, "drag_and_drop_verification_failure")
        raise e

if __name__ == "__main__":
    pytest.main()
