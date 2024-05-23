import pytest
import sys
import os

# Ajouter le répertoire contenant app.py au chemin de recherche Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Course

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_courses.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_get_courses(client):
    rv = client.get('/courses')
    assert rv.status_code == 200
    assert rv.json == []

def test_add_course_as_professor(client):
    rv = client.post('/courses', json={'title': 'Test Course', 'description': 'Test Description'}, headers={'Role': 'professor'})
    assert rv.status_code == 201
    assert rv.json['title'] == 'Test Course'
    assert rv.json['description'] == 'Test Description'

def test_add_course_as_student(client):
    rv = client.post('/courses', json={'title': 'Test Course', 'description': 'Test Description'}, headers={'Role': 'student'})
    assert rv.status_code == 403
    assert rv.json == {'error': 'Forbidden'}

def test_get_courses_with_data(client):
    client.post('/courses', json={'title': 'Test Course 1', 'description': 'Test Description 1'}, headers={'Role': 'professor'})
    client.post('/courses', json={'title': 'Test Course 2', 'description': 'Test Description 2'}, headers={'Role': 'professor'})
    rv = client.get('/courses')
    assert rv.status_code == 200
    courses = rv.json
    assert len(courses) == 2
    assert courses[0]['title'] == 'Test Course 1'
    assert courses[0]['description'] == 'Test Description 1'
    assert courses[1]['title'] == 'Test Course 2'
    assert courses[1]['description'] == 'Test Description 2'
