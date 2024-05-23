import pytest
import sys
import os
from flask import Flask
from unittest.mock import patch
import requests
import importlib.metadata

# Ajouter le répertoire contenant gateway_app.py au chemin de recherche Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gateway_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_forward_request(client):
    with patch('requests.request') as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"message": "success"}'
        mock_request.return_value = mock_response
        
        response = client.get('/students/test')
        
        mock_request.assert_called_once_with(
            method='GET',
            url='http://student:5002/test',
            headers={'User-Agent': 'Werkzeug/' + importlib.metadata.version("werkzeug")},
            json=None,
            allow_redirects=False
        )
        
        assert response.status_code == 200
        assert response.data == b'{"message": "success"}'

def test_student_service(client):
    with patch('requests.request') as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"message": "student service success"}'
        mock_request.return_value = mock_response
        
        response = client.get('/students/somepath')
        
        mock_request.assert_called_once_with(
            method='GET',
            url='http://student:5002/somepath',
            headers={'User-Agent': 'Werkzeug/' + importlib.metadata.version("werkzeug")},
            json=None,
            allow_redirects=False
        )
        
        assert response.status_code == 200
        assert response.data == b'{"message": "student service success"}'

def test_professor_service(client):
    with patch('requests.request') as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"message": "professor service success"}'
        mock_request.return_value = mock_response
        
        response = client.get('/professors/somepath')
        
        mock_request.assert_called_once_with(
            method='GET',
            url='http://professor:5003/somepath',
            headers={'User-Agent': 'Werkzeug/' + importlib.metadata.version("werkzeug")},
            json=None,
            allow_redirects=False
        )
        
        assert response.status_code == 200
        assert response.data == b'{"message": "professor service success"}'

def test_course_service(client):
    with patch('requests.request') as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"message": "course service success"}'
        mock_request.return_value = mock_response
        
        response = client.get('/courses/somepath')
        
        mock_request.assert_called_once_with(
            method='GET',
            url='http://course:5004/somepath',
            headers={'User-Agent': 'Werkzeug/' + importlib.metadata.version("werkzeug")},
            json=None,
            allow_redirects=False
        )
        
        assert response.status_code == 200
        assert response.data == b'{"message": "course service success"}'
