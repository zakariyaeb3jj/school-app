from flask import Flask, request
import requests

app = Flask(__name__)

def forward_request(service_url):
    response = requests.request(
        method=request.method,
        url=service_url,
        headers={key: value for key, value in request.headers.items() if key != 'Host'},
        json=request.get_json(silent=True),
        allow_redirects=False)
    return response.content, response.status_code, response.headers.items()

@app.route('/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def student_service(path):
    return forward_request(f'http://student:5002/{path}')

@app.route('/professors/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def professor_service(path):
    return forward_request(f'http://professor:5003/{path}')

@app.route('/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def course_service(path):
    return forward_request(f'http://course:5004/{path}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
