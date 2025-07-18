from flask import Flask, render_template, request, redirect, session, url_for, flash
import psycopg2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="study_notebook",
    user="vishnu123",
    password="lC1wtmqfVfU0jHrNIkcbgmb6sjYFJK2V",
    host="dpg-d1seqsruibrs73ac16ig-a",
    port="5432"
)
cur = conn.cursor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if "user_email" not in session:
        return redirect("/login")

    email = session["user_email"]
    cur.execute("SELECT name, email, college_name, role FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    # Fetch all uploaded PDFs
    cur.execute("SELECT course, year, subject, filename FROM pdf_notes")
    notes = cur.fetchall()

    return render_template("index.html", user=user, notes=notes)

# -----------------------------------------
# Student & Admin Shared Registration Page
# -----------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        college = request.form['college']
        role = "student"

        if "admin_code" in request.form and request.form['admin_code'] == "MVVR":
            role = "admin"
        elif "admin_code" in request.form and request.form['admin_code'] != "":
            flash("Invalid admin code", "danger")
            return redirect('/register')

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect('/register')

        try:
            cur.execute("INSERT INTO users (name, email, password, college_name, role) VALUES (%s, %s, %s, %s, %s)",
                        (name, email, password, college, role))
            conn.commit()
            flash("Registered successfully! Please login.", "success")
            return redirect('/login')
        except:
            flash("Email already exists", "danger")
            return redirect('/register')

    return render_template("register.html")

# -----------------------------------------
# Student Login
# -----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user and user[5] == "student":
            session["user_email"] = user[2]
            session["role"] = user[5]
            return redirect('/')
        else:
            flash("Invalid credentials or not a student", "danger")
            return redirect('/login')

    return render_template("login.html")

# -----------------------------------------
# Admin Login
# -----------------------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user and user[5] == "admin":
            session["user_email"] = user[2]
            session["role"] = user[5]
            return redirect('/')
        else:
            flash("Invalid admin credentials", "danger")
            return redirect('/admin_login')

    return render_template("admin_login.html")

# -----------------------------------------
# Admin Registration (via separate form)
# -----------------------------------------
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        college = request.form['college']
        code = request.form['admin_code']

        if code != "MVVR":
            flash("Invalid admin code", "danger")
            return redirect('/admin_register')

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect('/admin_register')

        try:
            cur.execute("INSERT INTO users (name, email, password, college_name, role) VALUES (%s, %s, %s, %s, %s)",
                        (name, email, password, college, "admin"))
            conn.commit()
            flash("Admin registered successfully! Please login.", "success")
            return redirect('/admin_login')
        except:
            flash("Email already exists", "danger")
            return redirect('/admin_register')

    return render_template("admin_register.html")

# -----------------------------------------
# Logout
# -----------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# -----------------------------------------
# Admin PDF Upload
# -----------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
def upload_pdf():
    if "user_email" not in session or session.get("role") != "admin":
        flash("Unauthorized access", "danger")
        return redirect('/login')

    if request.method == "POST":
        course = request.form['course']
        year = request.form['year']
        subject = request.form['subject']
        file = request.files['pdf']

        if not file or not allowed_file(file.filename):
            flash("Invalid file format. Only PDF allowed.", "danger")
            return redirect('/upload')

        if file.content_length and file.content_length > MAX_FILE_SIZE:
            flash("File is too large. Max 25MB allowed.", "danger")
            return redirect('/upload')

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cur.execute("INSERT INTO pdf_notes (course, year, subject, filename, uploaded_by) VALUES (%s, %s, %s, %s, %s)",
                    (course, year, subject, filename, session["user_email"]))
        conn.commit()

        flash("PDF uploaded successfully!", "success")
        return redirect('/')

    return render_template("upload.html")

# -----------------------------------------
# Start App
# -----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
