import pytest
import sys
import os

# Ajouter le répertoire contenant app.py au chemin de recherche Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Student

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_students_empty(client):
    rv = client.get('/students')
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_add_student(client):
    rv = client.post('/students', json={
        'name': 'Test Student',
        'email': 'test@student.com',
        'password': 'password'
    })
    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data['name'] == 'Test Student'
    assert json_data['email'] == 'test@student.com'
    assert json_data['role'] == 'student'

    rv = client.get('/students')
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data[0]['name'] == 'Test Student'

def test_add_duplicate_student(client):
    client.post('/students', json={
        'name': 'Test Student',
        'email': 'test@student.com',
        'password': 'password'
    })
    rv = client.post('/students', json={
        'name': 'Test Student',
        'email': 'test@student.com',
        'password': 'password'
    })
    assert rv.status_code == 400
    json_data = rv.get_json()
    assert 'error' in json_data

def test_login_student(client):
    client.post('/students', json={
        'name': 'Test Student',
        'email': 'test@student.com',
        'password': 'password'
    })
    rv = client.post('/students/login', json={
        'email': 'test@student.com',
        'password': 'password'
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['name'] == 'Test Student'
    assert json_data['email'] == 'test@student.com'
    assert json_data['role'] == 'student'

def test_login_student_invalid_credentials(client):
    client.post('/students', json={
        'name': 'Test Student',
        'email': 'test@student.com',
        'password': 'password'
    })
    rv = client.post('/students/login', json={
        'email': 'test@student.com',
        'password': 'wrongpassword'
    })
    assert rv.status_code == 401
    json_data = rv.get_json()
    assert 'error' in json_data
