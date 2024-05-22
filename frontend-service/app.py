from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    if 'role' in session:
        if session['role'] == 'student':
            return redirect(url_for('view_courses'))
        elif session['role'] == 'professor':
            return redirect(url_for('manage_courses'))
    return render_template('index.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = requests.post('http://student:5002/students/login', json={'email': email, 'password': password})
        if response.status_code == 200:
            session['role'] = 'student'
            session['user'] = response.json()
            return redirect(url_for('view_courses'))
        return render_template('student_login.html', error='Invalid credentials')
    return render_template('student_login.html')

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        response = requests.post('http://student:5002/students', json={'name': name, 'email': email, 'password': password})
        if response.status_code == 201:
            return redirect(url_for('student_login'))
        return render_template('student_signup.html', error=response.json().get('error', 'Error signing up'))
    return render_template('student_signup.html')

@app.route('/professor/login', methods=['GET', 'POST'])
def professor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = requests.post('http://professor:5003/professors/login', json={'email': email, 'password': password})
        if response.status_code == 200:
            session['role'] = 'professor'
            session['user'] = response.json()
            return redirect(url_for('manage_courses'))
        return render_template('professor_login.html', error='Invalid credentials')
    return render_template('professor_login.html')

@app.route('/professor/signup', methods=['GET', 'POST'])
def professor_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        response = requests.post('http://professor:5003/professors', json={'name': name, 'email': email, 'password': password})
        if response.status_code == 201:
            return redirect(url_for('professor_login'))
        return render_template('professor_signup.html', error=response.json().get('error', 'Error signing up'))
    return render_template('professor_signup.html')

@app.route('/courses', methods=['GET'])
def view_courses():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('home'))
    response = requests.get('http://course:5004/courses', headers={'Role': 'student'})
    if response.status_code == 200:
        courses = response.json()
        return render_template('courses.html', courses=courses)
    return render_template('courses.html', error='Could not fetch courses')

@app.route('/manage_courses', methods=['GET', 'POST'])
def manage_courses():
    if 'role' not in session or session['role'] != 'professor':
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        response = requests.post('http://course:5004/courses', json={'title': title, 'description': description}, headers={'Role': 'professor'})
        if response.status_code == 201:
            return redirect(url_for('manage_courses'))
    response = requests.get('http://course:5004/courses', headers={'Role': 'professor'})
    if response.status_code == 200:
        courses = response.json()
        return render_template('manage_courses.html', courses=courses)
    return render_template('manage_courses.html', error='Could not fetch courses')

@app.route('/logout')
def logout():
    session.pop('role', None)
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
