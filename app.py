from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, static_url_path='/static')

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

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user and check_password_hash(user[0], password):
         session['user'] = username
         return redirect(url_for('language'))
    else:
         flash("Invalid username or password")
         return redirect(url_for('index'))
 
    #if user:
        #return redirect(url_for('videos'))
     #   return redirect(url_for('language'))
    #else:
     #   return "Invalid username or password"


@app.route('/language', methods=['GET', 'POST'])
def language():
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
    return render_template('documents.html')

@app.route('/videos')
def videos():
    if 'user' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('index'))
    return render_template('videos.html')
    #return render_template('videos.html')

@app.route('/videos_en')
def videos_en():
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
                return "Username already exists"
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                return "Registration successful!"
        except Exception as e:
            db.rollback()
            return f"Error occurred: {str(e)}"
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

