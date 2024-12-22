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

## **Screenshots**

1. **Overview Task Progression**
   
   <img src="https://github.com/user-attachments/assets/2ebee150-8496-4b32-bacf-3709a4a98ff7" alt="Overview Task Progression" width="50%">

2. **User Stories**
   
   <img src="https://github.com/user-attachments/assets/48098201-d296-46e2-aa97-e42192838f43" alt="User Stories 1" width="50%">  

3. **Created vs Resolved Chart**
   
   <img src="https://github.com/user-attachments/assets/bc7fdfa4-b8c2-4e86-9dae-8c6807d85d54" alt="Created vs Resolved Chart" width="50%">

5. **Cumulative Flow Diagram**
   
   <img src="https://github.com/user-attachments/assets/003fdb63-ba56-4c54-a8c5-f64fca872315" alt="Cumulative Flow Diagram" width="50%">

7. **Issue Statistics (Change Type)**
   
   <img src="https://github.com/user-attachments/assets/2abaca78-1b1f-40a0-83d3-d6d3f11becc8" alt="Issue Statistics (Change Type)" width="50%">

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
