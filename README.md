# **Selenium Automation for Trello**

This repository features automated test scripts built with Selenium and Python to validate key functionalities of the [Trello](https://trello.com/) web application. This project demonstrates end-to-end testing, ensuring seamless user experiences and robust system reliability.

---

## **Project Overview**

### **Key Objectives**
- Automate login testing for valid and invalid credentials.
- Test the creation and management of boards, lists, and cards.
- Validate drag-and-drop functionality for cards between lists.
- Ensure dashboard UI elements (filtering, labeling, and search) function as intended.

---

## **Setup Instructions**

1. Clone the repository:  
   ```bash
   git clone https://github.com/raghav-narayan/selenium.git
   cd selenium
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Execute tests:  
   ```bash
   pytest --html=report.html
   ```

4. View the test report:  
   Open `report.html` in your browser.

---

## **Test Scenarios**

1. **Login Functionality**  
   - Valid credentials: Verifies successful login.  
   - Invalid credentials: Ensures proper error handling.

2. **Board, List, and Card Management**  
   - Automates creation and verification of boards, lists, and cards post-login.

3. **Drag-and-Drop Functionality**  
   - Validates moving cards between lists seamlessly.

4. **Dashboard and Features Validation**  
   - Confirms the visibility and usability of UI elements like filtering, labeling, and search.

---

## **Folder Structure**

```plaintext
selenium/
├── tests/
│   ├── test_login.py
│   ├── test_boards.py
│   ├── test_drag_and_drop.py
│   ├── test_dashboard_elements.py
│   ├── test_filter_label_search.py
├── screenshots/
│   ├── login_test.png
│   ├── board_creation.png
│   ├── drag_and_drop.png
│   ├── filter_search.png
├── requirements.txt
├── report.html
└── README.md
```

---

## **Screenshots**

Below are sample screenshots from test execution:

- **Login Test**
   ![image](https://github.com/user-attachments/assets/8e52e10b-c35c-40cf-9881-50ad2ffaa49f)

- **Board Creation**
   ![image](https://github.com/user-attachments/assets/cd732e45-9a1b-46cc-a801-c1c07e40f101)

- **Drag-and-Drop**
  ![image](https://github.com/user-attachments/assets/9fb06854-b30d-4971-a71f-50d588b59c64)

  ![image](https://github.com/user-attachments/assets/80d757d3-a07c-4611-af05-14fd5a55411d)

- **Filter and Search**  
  ![image](https://github.com/user-attachments/assets/e69c5380-20cf-4cd1-b1c4-4a5947344b7e)

  ![image](https://github.com/user-attachments/assets/56668b48-bd8b-4aff-8392-9e028f5512a6)

## **Future Enhancements**

- Add cross-browser testing support.
- Integrate CI/CD pipelines for automated test execution.
- Expand test scenarios for advanced Trello functionalities.

---

This repository highlights the application of automation in testing and serves as an ideal example of maintaining software quality at scale.
