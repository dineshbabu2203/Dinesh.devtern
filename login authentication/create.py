from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

secret = os.urandom(24)


app = Flask(__name__)
app.secret_key = secret

# Function to establish database connection
def get_db_connection():
    conn = sqlite3.connect('users_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for login page
@app.route('/')
def login():
    return render_template('login.html')

# Route for authenticating user
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')

# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
