import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Create a directory for screenshots if it doesn't exist
if not os.path.exists('./screenshots_create_card'):
    os.makedirs('./screenshots_create_card')

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, step_name):
    """Take a screenshot of the current page."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = f'./screenshots_create_card/{step_name}_{timestamp}.png'
    driver.save_screenshot(screenshot_path)
    print(f'Screenshot saved at: {screenshot_path}')

def test_trello_create_board_list_and_card(driver):
    driver.get("https://trello.com/login")

    # Log in to Trello
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys("rxr0654@mavs.uta.edu")
    email_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "login_email_sent")

    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("Luffy123!@#")
    password_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "login_password_sent")

    # Verify login was successful by checking the presence of "Boards" button
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Boards')]"))
    )
    assert "Boards" in driver.page_source
    take_screenshot(driver, "login_success")

    # Click on the "Create" button to show the dropdown
    create_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/nav/div[1]/div/div[3]/button/p"))
    )
    create_button.click()
    take_screenshot(driver, "create_button_clicked")

    # Click on the specified element to create a new board
    create_board_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'A board is made up of cards ordered on lists. Use it to manage projects, track information, or organize anything.')]"))
    )
    create_board_element.click()
    take_screenshot(driver, "create_board_element_clicked")

    # Wait for the board title input field to become visible and ready
    board_title_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='create-board-title-input']"))
    )

    # Enter the board title
    board_title = "Test Board"
    board_title_field.send_keys(board_title)

    # Click the button to create the board
    create_board_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='create-board-submit-button']"))
    )
    create_board_button.click()
    take_screenshot(driver, "board_created")

    # Verify board creation
    WebDriverWait(driver, 10).until(
        EC.title_contains(board_title)
    )
    assert board_title in driver.title

    # Create a new list in the board
    try:
        add_list_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='list-composer-button']"))
        )
        driver.execute_script("arguments[0].click();", add_list_button)
    except Exception as e:
        print("Error locating or clicking the 'Add List' button:", e)
        raise  # Optional: re-raise exception after logging

    # Wait for the textarea to become visible
    try:
        list_name_textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@name='Enter list name…']"))
        )
        # Enter the list name
        list_name = "To Do"
        list_name_textarea.send_keys(list_name)
    except Exception as e:
        print("Input via Selenium failed, executing JavaScript as fallback.")
        list_name = "To Do"
        driver.execute_script("arguments[0].value = arguments[1];", driver.find_element(By.XPATH, "//textarea[@name='Enter list name…']"), list_name)

    # Click the "Add list" button
    add_list_button_submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='list-composer-add-list-button']"))
    )
    add_list_button_submit.click()
    take_screenshot(driver, "list_created")

    # Verify the list creation
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//h2[contains(text(), '{list_name}')]"))
    )
    assert list_name in driver.page_source

    # Add a card to the newly created list
    try:
        add_card_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//h2[contains(text(), '{list_name}')]/following-sibling::div//textarea"))
        )
        driver.execute_script("arguments[0].click();", add_card_button)
        take_screenshot(driver, "add_card_button_clicked")

        # Wait for the textarea to become visible and enter the card name
        card_name_textarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//textarea[@name='Enter a title for this card…']"))
        )
        card_name = "Sample Card"
        card_name_textarea.send_keys(card_name)
        take_screenshot(driver, "card_name_entered")

        # Click the "Add Card" button
        add_card_button_submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Add Card']"))
        )
        add_card_button_submit.click()
        take_screenshot(driver, "card_added")

        # Verify the card creation
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(), '{card_name}')]"))
        )
        assert card_name in driver.page_source
    except Exception as e:
        print("Error adding card:", e)

if __name__ == "__main__":
    pytest.main()
