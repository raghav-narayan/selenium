# **Selenium Automation for Trello**  

This repository contains automated test scripts for verifying key functionalities of the [Trello](https://trello.com/) web application using Selenium and Python.  

---

## **Project Overview**

### **Key Objectives**
- Validate login functionality for valid and invalid credentials.  
- Test the creation and management of boards, lists, and cards.  
- Verify drag-and-drop functionality for cards between lists.  
- Check dashboard UI elements and key functionalities (filtering, labeling, and search).  

---

## **Test Scenarios**

1. **Login Functionality**  
   - Valid credentials: Successful login.  
   - Invalid credentials: Proper error handling.  

2. **Board, List, and Card Management**  
   - Automates creation and management post-login.  

3. **Drag-and-Drop Functionality**  
   - Move cards between lists.  

4. **Dashboard and Features Validation**  
   - Verify UI elements, filtering, labeling, and search.  

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

3. Run tests:  
   ```bash
   pytest --html=report.html
   ```

4. View test reports:  
   - Open `report.html` in your browser.  

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
├── requirements.txt
└── README.md
```

---

## **Future Enhancements**

- Add cross-browser compatibility.  
- Implement CI/CD pipelines for automated test execution.  
