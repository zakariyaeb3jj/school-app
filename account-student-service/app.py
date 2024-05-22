from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'email': s.email, 'role': s.role} for s in students])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    new_student = Student(name=data['name'], email=data['email'], password=data['password'], role='student')
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'id': new_student.id, 'name': new_student.name, 'email': new_student.email, 'role': new_student.role}), 201

@app.route('/students/login', methods=['POST'])
def login_student():
    data = request.json
    student = Student.query.filter_by(email=data['email'], password=data['password']).first()
    if student:
        return jsonify({'id': student.id, 'name': student.name, 'email': student.email, 'role': student.role}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
