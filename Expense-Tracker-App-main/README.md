# Expense Tracker App

A professional full-stack web application for managing personal expenses. This app includes a public landing page, secure user authentication, expense management with filtering, dashboard visualization using Chart.js, and CSV export functionality. 
## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contact](#contact)

## Features

- **Public Homepage:**  
  A welcoming landing page with clear call-to-action buttons for login and registration.

- **User Authentication:**  
  Secure registration, login, and logout functionality using Flask-Login. Each user has their own expense list.

- **Expense Management:**  
  Users can add, view, edit, and delete expenses. Each expense is tied to the authenticated user.

- **Expense Filtering:**  
  Filter expenses by specifying a start and end date.

- **Dashboard Visualization:**  
  An interactive dashboard with a responsive pie chart (powered by Chart.js) that summarizes expenses by category.

- **CSV Export:**  
  Export expense data as a CSV file for further analysis.

- **Responsive Design:**  
  Built with Bootstrap 5 to ensure a seamless experience on all devices.

## Technologies Used

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, SQLAlchemy  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5, Chart.js  
- **Others:** Python’s CSV module for data export  

## Installation

### Prerequisites

- Python 3.x installed on your system.
- Git (optional, for cloning the repository).

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Abdullah92o/Expense-Tracker-App.git
   cd Expense-Tracker-App
   ```

2. **Set Up a Virtual Environment:**

   - **On Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   python app.py
   ```

5. **Access the Application:**

   Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage

- **Public Homepage:**  
  Visit `/` to see a welcoming landing page with options to log in or register.

- **User Registration and Login:**  
  - Register at `/register`
  - Log in at `/login` to access your expense dashboard.

- **Expense Management:**  
  - View and manage expenses at `/expenses`
  - Use the filtering form to search expenses by date range.
  - Add, edit, or delete expenses.

- **Dashboard:**  
  - Visit `/dashboard` to view a pie chart summarizing expenses by category.

- **CSV Export:**  
  - Click the "Export CSV" button to download your expense data.

## Project Structure

```
expense_tracker/
├── app.py                  # Main Flask application file
├── requirements.txt        # List of project dependencies
├── static/
│   ├── style.css           # Custom CSS styles
├── templates/              # HTML templates
│   ├── layout.html         # Base template with Bootstrap and dynamic navbar
│   ├── home.html           # Public landing page
│   ├── expenses.html       # Expense management page for authenticated users
│   ├── add_expense.html    # Form for adding a new expense
│   ├── edit_expense.html   # Form for editing an existing expense
│   ├── dashboard.html      # Dashboard with a Chart.js pie chart
│   ├── login.html          # User login form
│   ├── register.html       # User registration form
```

## Future Enhancements

- **Password Reset Functionality:**  
  Implement a secure password recovery/reset feature.

- **Enhanced Analytics:**  
  Add more detailed reporting features (e.g., monthly summaries, trend analysis).

- **Mobile Optimization:**  
  Improve the responsive design for better mobile usability.

- **Cloud Deployment:**  
  Deploy the application to a cloud platform (e.g., Heroku, AWS) for public access.

## License

This project is licensed under the MIT License.

## Contact

For further inquiries or suggestions :
Here at Github

---

**Happy Coding! 🚀**
