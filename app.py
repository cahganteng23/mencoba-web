from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'rahasia123'

USER_FILE = 'users.json'
BLOG_FILE = 'blog.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE) as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def load_blog():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE) as f:
            return json.load(f)
    return {"title": "Selamat Datang", "content": "Ini adalah konten awal."}

def save_blog(blog):
    with open(BLOG_FILE, 'w') as f:
        json.dump(blog, f)

@app.route('/')
def index():
    blog = load_blog()
    return render_template('index.html', blog=blog)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password and users[username]['role'] == role:
            session['username'] = username
            session['role'] = role
            return redirect('/dashboard' if role == 'admin' else '/')
        return 'Login gagal!'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        users = load_users()
        users[username] = {'password': password, 'role': role}
        save_users(users)
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect('/')
    blog = load_blog()
    if request.method == 'POST':
        blog['title'] = request.form['title']
        blog['content'] = request.form['content']
        save_blog(blog)
        return redirect('/')
    return render_template('dashboard.html', blog=blog)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
