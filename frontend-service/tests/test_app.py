import pytest
import sys
import os
from flask import session

# Ajouter le répertoire contenant app.py au chemin de recherche Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'your_secret_key'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_student_login_page(client):
    rv = client.get('/student/login')
    assert rv.status_code == 200
    assert b'Student Login' in rv.data

def test_professor_login_page(client):
    rv = client.get('/professor/login')
    assert rv.status_code == 200
    assert b'Professor Login' in rv.data

def test_student_signup_page(client):
    rv = client.get('/student/signup')
    assert rv.status_code == 200
    assert b'Student Sign Up' in rv.data

def test_professor_signup_page(client):
    rv = client.get('/professor/signup')
    assert rv.status_code == 200
    assert b'Professor Sign Up' in rv.data

def test_student_login(client, monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {'id': 1, 'name': 'Test Student', 'email': 'test@student.com', 'role': 'student'}
        status_code = 200

    def mock_post(url, json):
        return MockResponse()

    monkeypatch.setattr('requests.post', mock_post)

    rv = client.post('/student/login', data={'email': 'test@student.com', 'password': 'password'})
    assert rv.status_code == 302
    with client.session_transaction() as sess:
        assert sess['role'] == 'student'

def test_professor_login(client, monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {'id': 1, 'name': 'Test Professor', 'email': 'test@professor.com', 'role': 'professor'}
        status_code = 200

    def mock_post(url, json):
        return MockResponse()

    monkeypatch.setattr('requests.post', mock_post)

    rv = client.post('/professor/login', data={'email': 'test@professor.com', 'password': 'password'})
    assert rv.status_code == 302
    with client.session_transaction() as sess:
        assert sess['role'] == 'professor'

def test_view_courses(client, monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return [{'id': 1, 'title': 'Test Course', 'description': 'Test Description'}]
        status_code = 200

    def mock_get(url, headers):
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_get)

    with client.session_transaction() as sess:
        sess['role'] = 'student'

    rv = client.get('/courses')
    assert rv.status_code == 200
    assert b'Test Course' in rv.data

def test_manage_courses(client, monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return [{'id': 1, 'title': 'Test Course', 'description': 'Test Description'}]
        status_code = 200

    def mock_get(url, headers):
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_get)

    with client.session_transaction() as sess:
        sess['role'] = 'professor'

    rv = client.get('/manage_courses')
    assert rv.status_code == 200
    assert b'Test Course' in rv.data
