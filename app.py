from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')  # Secret key for session management

# MySQL Connection
db = mysql.connector.connect(
    host="database-1.c3qmsqu6ilty.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Redhat123",
    database="myproject"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    
    if user and check_password_hash(user[0], password):
        session['user'] = username
        print("User logged in:", username) 
        return redirect(url_for('language'))
    else:
        flash("Invalid username or password")
        print("Login failed for:", username) 
        return redirect(url_for('index'))

@app.route('/language', methods=['GET', 'POST'])
def language():
    if 'user' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        language = request.form['language']
        if language == 'tamil':
            return redirect(url_for('videos'))
        elif language == 'english':
            return redirect(url_for('videos_en'))
        else:
            return "Invalid language selection"
    return render_template('language.html')

@app.route('/documents')
def documents():
    if 'user' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('index'))
    return render_template('documents.html')

@app.route('/videos')
def videos():
    if 'user' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('index'))
    return render_template('videos.html')

@app.route('/videos_en')
def videos_en():
    if 'user' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('index'))
    return render_template('videos_en.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Username already exists")
                return redirect(url_for('register'))
            else:
                hashed_password = generate_password_hash(password)
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                db.commit()
                flash("Registration successful!")
                return redirect(url_for('index'))
        except Exception as e:
            db.rollback()
            flash(f"Error occurred: {str(e)}")
            return redirect(url_for('register'))
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session
    flash("You have been logged out.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
