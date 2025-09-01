# Health-Records-PLP_Hack

A **subscription-based health record management system** for schools to digitally track students’ health information. Built as part of the **Power Learn Project (PLP) Hackathon** under the **Good Health and Well-Being (SDG 3)** theme.

---

##  Features

- **School Registration** – Secure onboarding for schools into the system.
- **Student Management** – Easily add and manage student profiles.
- **Health Record Tracking** – Log student wellness data (like health incidents, checkups, notes).
- **MySQL Storage** – Robust, persistent storage for all records.
- **CORS Support** – Seamless frontend/backend communication using Flask & Flask-CORS.

---

##  Tech Stack

| Component   | Technology                      |
|-------------|---------------------------------|
| Frontend    | HTML, CSS, JavaScript           |
| Backend     | Python with Flask               |
| Database    | MySQL (with `mysql-connector`)  |
| API Support | `flask-cors` for cross-origin   |

---

##  Project Structure

hackathon/
├── index.html # Main UI page
├── style.css # Styling for the frontend
├── script.js # JavaScript logic for form actions
├── backend.py # Flask-based API server
└── setup.sql # SQL script to create required DB and tables



---

##  Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/0xdave1/Health-Records-PLP_Hack.git
   cd Health-Records-PLP_Hack
2. Set up the database:

Log into MySQL and run the SQL commands in setup.sql to create your school_health database with necessary tables.

3.Install the backend dependencies:

   pip install flask flask-cors mysql-connector-python

4. Configure backend.py to match your MySQL credentials:
   db = mysql.connector.connect(
  host="localhost",
  user="YOUR_DB_USER",
  password="YOUR_DB_PASSWORD",
  database="school_health"
)

5. Run the backend server:

   python backend.py

6. Open index.html in your browser and use the app.
