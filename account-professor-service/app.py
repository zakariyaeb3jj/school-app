from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='professor')

@app.route('/professors', methods=['GET'])
def get_professors():
    professors = Professor.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'email': p.email, 'role': p.role} for p in professors])

@app.route('/professors', methods=['POST'])
def add_professor():
    data = request.json
    if Professor.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    new_professor = Professor(name=data['name'], email=data['email'], password=data['password'], role='professor')
    db.session.add(new_professor)
    db.session.commit()
    return jsonify({'id': new_professor.id, 'name': new_professor.name, 'email': new_professor.email, 'role': new_professor.role}), 201

@app.route('/professors/login', methods=['POST'])
def login_professor():
    data = request.json
    professor = Professor.query.filter_by(email=data['email'], password=data['password']).first()
    if professor:
        return jsonify({'id': professor.id, 'name': professor.name, 'email': professor.email, 'role': professor.role}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003, debug=True)
