import pytest
from app import app, db, Professor

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_professors.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_professors(client):
    """Test the GET /professors route."""
    rv = client.get('/professors')
    assert rv.status_code == 200
    assert rv.json == []

def test_add_professor(client):
    """Test the POST /professors route."""
    rv = client.post('/professors', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert rv.status_code == 201
    assert rv.json['name'] == 'John Doe'
    assert rv.json['email'] == 'john.doe@example.com'

def test_add_professor_duplicate_email(client):
    """Test the POST /professors route with duplicate email."""
    client.post('/professors', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    rv = client.post('/professors', json={
        'name': 'Jane Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert rv.status_code == 400
    assert rv.json['error'] == 'Email already registered'

def test_login_professor(client):
    """Test the POST /professors/login route."""
    client.post('/professors', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    rv = client.post('/professors/login', json={
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert rv.status_code == 200
    assert rv.json['email'] == 'john.doe@example.com'

def test_login_professor_invalid(client):
    """Test the POST /professors/login route with invalid credentials."""
    client.post('/professors', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    rv = client.post('/professors/login', json={
        'email': 'john.doe@example.com',
        'password': 'wrongpassword'
    })
    assert rv.status_code == 401
    assert rv.json['error'] == 'Invalid credentials'
