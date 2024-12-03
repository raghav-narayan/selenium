import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

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

def test_add_green_label_to_card(driver):
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

    # Step 2: Navigate to your Trello board
    driver.get("https://trello.com/b/GH3SE4Yw/my-trello-board")
    take_screenshot(driver, "navigated_to_board")  # Screenshot after navigating to board

    # Step 3: Click on the "Requirements Gathering" card
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@data-testid='card-name' and text()='Requirements Gathering']"))
    )

    # Using try-except block to handle StaleElementReferenceException if it occurs
    try:
        card = driver.find_element(By.XPATH, "//a[@data-testid='card-name' and text()='Requirements Gathering']")
        card.click()
    except StaleElementReferenceException:
        card = driver.find_element(By.XPATH, "//a[@data-testid='card-name' and text()='Requirements Gathering']")
        card.click()
    
    take_screenshot(driver, "card_clicked")  # Screenshot after clicking the card

    # Step 4: Click on the "Labels" button in the modal
    labels_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='card-back-labels-button']"))
    )
    labels_button.click()
    take_screenshot(driver, "labels_button_clicked")  # Screenshot after clicking labels button

    # Step 5: Select the green label
    green_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-color='green' and @data-testid='card-label']"))
    )
    green_label.click()
    take_screenshot(driver, "green_label_selected")  # Screenshot after selecting green label

    close_modal_button_xpath = "//span[@data-testid='CloseIcon']"
    for attempt in range(3):  # Attempt up to 3 times in case of StaleElementReferenceException
        try:
            close_modal_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, close_modal_button_xpath))
            )
            close_modal_button.click()
            take_screenshot(driver, "modal_closed")  # Screenshot after closing the modal
            break  # Exit the loop if click is successful
        except StaleElementReferenceException:
            time.sleep(1)  # Wait briefly before retrying
        except Exception as e:
            print(f"Error clicking the close button: {e}")
            break  # Break the loop on unexpected exceptions

    time.sleep(2)  # Ensure the modal has closed

    # Re-locate the card element to ensure it has been updated
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@data-testid='card-name' and text()='Requirements Gathering']"))
    )

    # Verify if the green label is displayed on the card
    try:
        updated_card = driver.find_element(By.XPATH, "//a[@data-testid='card-name' and text()='Requirements Gathering']/ancestor::div//span[contains(@class, 'color-blind-pattern-green')]")
        assert updated_card.is_displayed(), "Green label was not added to the card."
        take_screenshot(driver, "green_label_verified")  # Screenshot after verifying the label
    except StaleElementReferenceException:
        updated_card = driver.find_element(By.XPATH, "//a[@data-testid='card-name' and text()='Requirements Gathering']/ancestor::div//span[contains(@class, 'color-blind-pattern-green')]")
        assert updated_card.is_displayed(), "Green label was not added to the card."
        take_screenshot(driver, "green_label_verified_after_exception")  # Screenshot after verifying the label after exception

if __name__ == "__main__":
    pytest.main()
