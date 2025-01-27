import json
from flask import Flask
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from core import db
from core.models.assignments import Assignment
from core.libs.exceptions import FyleError
from core.server import handle_error, app

def test_ready_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'
    assert 'time' in data

def test_handle_fyle_error(client, h_student_1):
    # Submit an assignment with a non-existent ID to trigger FyleError
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 9999,  # Assuming this ID does not exist
            'teacher_id': 1
        }
    )
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'FyleError'

def test_handle_validation_error(client, h_student_1):
    # Create an assignment with invalid data
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None  # Invalid as content is required
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'ValidationError'

from sqlalchemy.exc import IntegrityError
from core import db
from core.models.assignments import Assignment

# def test_handle_integrity_error(client):
#     # Create first assignment
#     assignment1 = Assignment(id=1, student_id=1, content='First', state='DRAFT')
#     db.session.add(assignment1)
#     db.session.commit()

#     # Try to create duplicate assignment
#     assignment2 = Assignment(id=1, student_id=1, content='Duplicate ID', state='DRAFT')
#     db.session.add(assignment2)

#     try:
#         db.session.commit()
#     except IntegrityError as err:
#         db.session.rollback()
#         # handle_error returns tuple (response, status_code)
#         response, status_code = handle_error(err)
#         assert status_code == 400
#         data = json.loads(response.get_data(as_text=True))
#         assert data['error'] == 'IntegrityError'

def test_handle_http_exception(client):
    response = client.get('/non-existent-endpoint')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'NotFound'

def test_fyle_error_to_dict():
    error = FyleError(status_code=400, message='Test error message')
    error_dict = error.to_dict()
    assert error_dict == {'message': 'Test error message'}

def test_assert_auth_failure(client):
    response = client.get('/student/assignments')
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'principal not found'


def test_assert_true_failure(client):
    # Use teacher credentials to access a student endpoint
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }
    response = client.get('/student/assignments', headers=headers)
    assert response.status_code == 403
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'requester should be a student'