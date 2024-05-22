from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in courses])

@app.route('/courses', methods=['POST'])
def add_course():
    role = request.headers.get('Role')
    if role != 'professor':
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json
    new_course = Course(title=data['title'], description=data['description'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'id': new_course.id, 'title': new_course.title, 'description': new_course.description}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5004, debug=True)
