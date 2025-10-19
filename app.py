from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash # Using Werkzeug for hashing
import os, re, PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# =========================
# ⚙️ APP AND CONFIGURATION
# =========================
app = Flask(__name__)
# 🛑 CONSOLIDATED CONFIGURATION 🛑
# 🛑 NEW (MySQL/MariaDB via XAMPP) 🛑
# Ensure XAMPP's MySQL service is running, and the database 'ai_resume_db' exists.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ai_resume_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_super_secret_key_change_me' # Use a real secret key in production

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."

# 📁 Create folders
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "generated_reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# =========================
# 👤 USER MODEL (Flask-SQLAlchemy)
# =========================
class User(db.Model, UserMixin): # Inherits from db.Model and UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Method to set the password securely using Werkzeug
    def set_password(self, password):
    # Use a consistent hashing algorithm
     self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        
    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Flask-Login user_loader function
@login_manager.user_loader
def load_user(user_id):
    # This now uses the SQLAlchemy User model
    return db.session.get(User, int(user_id)) 


# =========================
# 🧾 ROUTES
# =========================
@app.route('/')
def home():
    # Assuming 'index.html' is where you have the upload form or a welcome screen
    return render_template('index.html')



# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("⚠️ Username already exists.")
            return redirect(url_for('register'))

        # Create new user and hash the password
        new_user = User(username=username)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("✅ Registration successful! Please log in.")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "error")

    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        print("DEBUG: Username entered:", username)
        print("DEBUG: Password entered:", password)
        print("DEBUG: User fetched:", user)

        if user:
            print("DEBUG: Stored hash:", user.password_hash)
            print("DEBUG: Password match?", user.check_password(password))

        if user and user.check_password(password):
            login_user(user)
            flash("✅ Logged in successfully!")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash("❌ Invalid username or password.")
            
    return render_template('login.html')


# ---------- LOGOUT ----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 Logged out successfully.")
    return redirect(url_for('login'))

# ---------- ANALYZE RESUME (Your existing logic) ----------
@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    # ... (Your existing resume analysis logic is placed here) ...
    file = request.files['resume']
    if not file:
        flash("⚠️ No file selected!")
        return redirect(url_for('home'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    flash("✅ Resume uploaded successfully!")

    # Extract text
    text = ""
    try:
        reader = PyPDF2.PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() or ""
        text = text.replace("\n", " ").replace("\r", " ")
    except Exception as e:
        flash(f"Error reading PDF: {e}", "error")
        return redirect(url_for('home'))


    # Extract skills
    skills = ["python", "java", "html", "css", "javascript", "sql", "django", "flask"]
    found_skills = [s for s in skills if re.search(rf'\b{s}\b', text, re.IGNORECASE)]

    # Job roles
    job_roles = {
        "Web Developer": ["html", "css", "javascript", "django"],
        "Data Analyst": ["python", "sql", "excel"],
        "AI Engineer": ["python", "machine learning", "nlp"]
    }

    matches = {}
    for job, req_skills in job_roles.items():
        common = set(found_skills) & set(req_skills)
        missing = list(set(req_skills) - set(found_skills))
        match_percent = round(len(common) / len(req_skills) * 100, 2)
        matches[job] = {"percent": match_percent, "missing_skills": missing}

    # Generate PDF
    pdf_filename = f"{current_user.username}_{os.path.splitext(file.filename)[0]}_report.pdf" # Include username in report name
    pdf_path = os.path.join(REPORT_FOLDER, pdf_filename)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    logo_path = os.path.join("static", "logo.png")
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 60, height - 80, width=70, height=50, mask='auto')

    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, height - 60, "AI Resume Analyzer Report")

    c.setStrokeColor(colors.darkblue)
    c.line(50, height - 90, width - 50, height - 90)

    y = height - 130
    c.setFont("Helvetica-Bold", 13)
    # 🛑 Use current_user from Flask-Login 🛑
    c.drawString(50, y, f"User: {current_user.username}")

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Extracted Skills:")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(70, y, ", ".join(found_skills) if found_skills else "No skills detected.")

    y -= 40
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Job Role Matching Results:")

    y -= 30
    for job, data in matches.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, f"{job}: {data['percent']}% Match")
        y -= 20
        c.setFont("Helvetica", 11)
        c.drawString(80, y, f"Missing Skills: {', '.join(data['missing_skills']) if data['missing_skills'] else 'None'}")
        y -= 30

    c.save()

    return render_template('result.html', found_skills=found_skills, matches=matches, pdf_filename=pdf_filename)


@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(REPORT_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    # 🛑 IMPORTANT: Create tables before running the app for the first time
    with app.app_context():
        db.create_all() 
    app.run(debug=True)