from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory
import psycopg2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure upload folder and max file size (25MB)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB

# PostgreSQL Database connection
conn = psycopg2.connect(
    dbname="study_notebook",
    user="vishnu123",
    password="lC1wtmqfVfU0jHrNIkcbgmb6sjYFJK2V",
    host="dpg-d1seqsruibrs73ac16ig-a",
    port="5432"
)
cur = conn.cursor()

# ---------- STUDENT ROUTES ----------

@app.route('/')
def home():
    if "user_email" not in session:
        return redirect("/login")

    # Fetch student details
    cur.execute("SELECT name, email, college_name FROM students WHERE email = %s", (session["user_email"],))
    student = cur.fetchone()

    # Fetch PDFs uploaded by admin
    cur.execute("SELECT course_name, year, subject, file_name FROM pdfs ORDER BY id DESC")
    pdfs = cur.fetchall()

    return render_template("index.html", student=student, pdfs=pdfs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        college = request.form['college']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect('/register')

        try:
            cur.execute("INSERT INTO students (name, email, password, college_name) VALUES (%s, %s, %s, %s)", 
                        (name, email, password, college))
            conn.commit()
            flash("Registered Successfully! Please login.", "success")
            return redirect('/login')
        except:
            flash("Email already exists", "danger")
            return redirect('/register')

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur.execute("SELECT * FROM students WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user:
            session["user_email"] = user[2]  # user[2] = email
            session["role"] = "student"
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/login')

    return render_template("login.html")

# ---------- ADMIN ROUTES ----------

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        code = request.form['admin_code']

        if code != "MVVR":
            flash("Invalid Admin Code", "danger")
            return redirect('/admin_register')

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect('/admin_register')

        try:
            cur.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", 
                        (name, email, password))
            conn.commit()
            flash("Admin Registered! Please login.", "success")
            return redirect('/admin_login')
        except:
            flash("Admin Email already exists", "danger")
            return redirect('/admin_register')

    return render_template("admin_register.html")


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur.execute("SELECT * FROM admins WHERE email = %s AND password = %s", (email, password))
        admin = cur.fetchone()

        if admin:
            session["admin_email"] = admin[2]
            session["role"] = "admin"
            return redirect('/admin_dashboard')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/admin_login')

    return render_template("admin_login.html")


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if "admin_email" not in session:
        return redirect('/admin_login')

    if request.method == "POST":
        course = request.form['course']
        year = request.form['year']
        subject = request.form['subject']
        file = request.files['pdf']

        if file and file.filename.endswith(".pdf"):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("INSERT INTO pdfs (course_name, year, subject, file_name) VALUES (%s, %s, %s, %s)",
                        (course, year, subject, filename))
            conn.commit()

            flash("PDF uploaded successfully", "success")
        else:
            flash("Only PDF files are allowed", "danger")

    return render_template("admin_dashboard.html")


@app.route('/uploads/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- END ----------

if __name__ == "__main__":
    app.run(debug=True)
