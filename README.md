# AI_Resume_Analyzer
AI_Resume_Analyzer Description
⚡ AI Résumé Analyzer ⚡
A secure, high-tech web application built with Flask that analyzes user-uploaded résumés (PDFs), extracts skills, calculates job match percentages against predefined roles, and generates a personalized, professional PDF report.

✨ Features
Secure Authentication: User registration and login managed by Flask-Login with passwords securely hashed using Werkzeug.

Database Integration: Uses MySQL (XAMPP) via Flask-SQLAlchemy for persistent storage of user accounts.

Résumé Processing: Extracts text from uploaded PDF files using PyPDF2.

Intelligent Matching: Calculates percentage match and identifies missing skills for three sample job roles (Web Developer, Data Analyst, AI Engineer).

Professional Reporting: Generates a detailed, downloadable PDF report using ReportLab for each analysis.

Animated UI: Modern, dark-themed user interface with CSS animations for a high-tech aesthetic.

🚀 Getting Started
Follow these steps to get a copy of the project running on your local machine.

Prerequisites
You need the following software installed:

Python 3.x

XAMPP (or equivalent MySQL/MariaDB server)

Virtual Environment (recommended)

Installation
Clone the repository:

Bash

git clone [YOUR_REPOSITORY_URL]
cd AI_Resume_Analyzer
Create and activate a virtual environment:

Bash

# Create
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
(Note: If you haven't created a requirements.txt, run pip freeze > requirements.txt now, or manually run: pip install Flask Flask-SQLAlchemy PyPDF2 ReportLab Flask-Login werkzeug pymysql mysqlclient)

🛠️ Setup: Database Configuration (XAMPP)
The application is configured to connect to a local MySQL server (XAMPP).

1. Start XAMPP Services
In your XAMPP Control Panel, click Start for both Apache and MySQL.

2. Create the Database
The application requires an empty database named ai_resume_db.

Open phpMyAdmin (usually by clicking the Admin button next to MySQL in XAMPP).

Click New on the left sidebar.

Enter the database name: ai_resume_db

Click Create.

3. Verify Connection String
Ensure the connection string in your app.py file is correct for your XAMPP setup (default root user with no password):

Python

# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ai_resume_db'
▶️ Running the Application
Ensure XAMPP MySQL is running.

Ensure your Python virtual environment is active.

Run the Flask application:

Bash

python app.py
Access the App: Open your web browser and navigate to:

http://127.0.0.1:5000/
The application will automatically connect to your MySQL database and create the user table when first run (db.create_all()).

📂 Project Structure
AI_Resume_Analyzer/
├── app.py                      # Main Flask application file (Routes, Models, Logic)
├── static/                     # Static files (CSS, images, etc.)
│   └── style.css               # Contains the animated glowing styles
├── templates/                  # Jinja2 HTML files
│   ├── index.html              # Main resume upload page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   └── result.html             # Analysis results page
├── uploads/                    # Uploaded resume files (ignored by Git)
├── generated_reports/          # Generated PDF reports (ignored by Git)
├── requirements.txt            # Project dependencies
└── README.md                   # This file
🤝 Contribution
If you have suggestions for new job roles, more advanced skill extraction, or performance improvements, please open an issue or submit a pull request!

📄 License
This project is licensed under the MIT License - see the LICENSE.md file for details.

📧 Contact
Pramod Maloji- pramodmaloji96@gmail.com

Project Link: https://github.com/pramodmalogi-007/AI_Resume_Analyzer
