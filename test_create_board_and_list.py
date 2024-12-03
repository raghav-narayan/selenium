import pytest
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a directory for screenshots if it doesn't exist
screenshot_dir = './screenshots_create_board_and_list'
os.makedirs(screenshot_dir, exist_ok=True)

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, step):
    screenshot_path = os.path.join(screenshot_dir, f"{step}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def test_trello_create_board_and_list(driver):
    driver.get("https://trello.com/login")
    take_screenshot(driver, "login_page")

    # Log in to Trello
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'username'))
    )
    email_field.send_keys("rxr0654@mavs.uta.edu")
    email_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "email_entered")

    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("Luffy123!@#")
    password_field.send_keys(Keys.ENTER)
    take_screenshot(driver, "password_entered")

    # Verify login was successful by checking the presence of "Boards" button
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Boards')]"))
    )
    assert "Boards" in driver.page_source
    take_screenshot(driver, "logged_in")

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
    take_screenshot(driver, "board_title_field_visible")

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
    take_screenshot(driver, "board_title_verified")

    # Create a new list in the board
    try:
        add_list_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='list-composer-button']"))
        )
        # Use JavaScript to click the button to avoid issues with overlays
        driver.execute_script("arguments[0].click();", add_list_button)
        take_screenshot(driver, "add_list_button_clicked")
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
        take_screenshot(driver, "list_name_entered")
    except Exception as e:
        # Fallback JavaScript execution if standard input fails
        print("Input via Selenium failed, executing JavaScript as fallback.")
        list_name = "To Do"
        driver.execute_script("arguments[0].value = arguments[1];", driver.find_element(By.XPATH, "//textarea[@name='Enter list name…']"), list_name)

    # Click the "Add list" button
    add_list_button_submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='list-composer-add-list-button']"))
    )
    add_list_button_submit.click()
    take_screenshot(driver, "add_list_button_submit_clicked")

    # Verify the list creation
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//h2[contains(text(), '{list_name}')]"))
    )
    assert list_name in driver.page_source
    take_screenshot(driver, "list_created")

if __name__ == "__main__":
    pytest.main()
