from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from werkzeug.utils import secure_filename

import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database connection
conn = psycopg2.connect(
    dbname="study_notebook",
    user="vishnu123",
    password="lC1wtmqfVfU0jHrNIkcbgmb6sjYFJK2V",
    host="dpg-d1seqsruibrs73ac16ig-a",
    port="5432"
)
cur = conn.cursor()
from flask import send_from_directory

@app.route('/static/pdfs/<path:filename>')
def serve_pdf(filename):
    return send_from_directory('static/pdfs', filename)
@app.route('/')
def home():
    if "user_email" not in session:
        return redirect("/login")

    # Fetch student details
    cur.execute("SELECT name, email, college_name FROM students WHERE email = %s", (session["user_email"],))
    student = cur.fetchone()

    # Fetch notes (optional or course list logic)
    cur.execute("SELECT * FROM pdfs")
    notes = cur.fetchall()

    return render_template("index.html", student=student, notes=notes)
   
# Ensure PDF upload folder exists
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'pdfs')
# Create the folder if it doesn't exist  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)    

# Admin Dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if "user_email" not in session:
        return redirect('/admin_login')
    # Fetch student details
    cur.execute("SELECT name, email, code FROM admins WHERE email = %s", (session["user_email"],))
    admin = cur.fetchone()    

    if request.method == 'POST':
        course = request.form['course']
        year = request.form['year']
        subject = request.form['subject']
        pdf_file = request.files['pdf_file']

        if pdf_file:
            filename = secure_filename(pdf_file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf_file.save(save_path)

            cur.execute("INSERT INTO pdfs (course, year, subject, filename) VALUES (%s, %s, %s, %s)",
                        (course, year, subject, filename))
            conn.commit()
            return redirect('/admin_dashboard')

    cur.execute("SELECT * FROM pdfs")
    pdfs = cur.fetchall()
    
    return render_template('admin_dashboard.html', admin=admin, pdfs=pdfs)

# Student Dashboard 


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
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/login')

    return render_template("login.html")
@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        code = request.form["code"]

        # 1. Check password match
        if password != confirm:
            flash("Passwords do not match!", "error")
            return render_template('/admin_register')
        try:
            cur.execute("INSERT INTO admins (name, email, password, code) VALUES (%s, %s, %s, %s)", 
                        (name, email, password, code))
            conn.commit()
            flash("Registered Successfully! Please login.", "success")
            return redirect('/admin_login')
        except:
            flash("Email already exists", "danger")
            return redirect('/admin_register')
            

        # 2. Check for valid admin code
        if code != "MVVR":
            flash("Invalid Admin Code. Please enter correct code.", "error")
            return render_template('/admin_register')

        

    return render_template("admin_register.html")
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur.execute("SELECT * FROM admins WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user:
            session["user_email"] = user[2]  # user[2] = email
            return redirect('/admin_dashboard')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/admin_login')

    return render_template("admin_login.html")    


@app.route('/get_pdfs/<course>')
def get_pdfs(course):
    cur.execute("SELECT year, subject, filename FROM pdfs WHERE course = %s", (course,))
    rows = cur.fetchall()

    pdfs = []
    for row in rows:
        year, subject, filename = row
        pdf_url = url_for('static', filename='pdfs/' + filename)
        pdfs.append({'year': year, 'subject': subject, 'pdf_url': pdf_url})

    return jsonify(pdfs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_note():
    if "user" not in session:
        return redirect('/login')
    title = request.form['title']
    content = request.form['content']
    cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

