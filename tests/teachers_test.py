from core.models.teachers import Teacher
from core.models.assignments import AssignmentStateEnum

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_teacher_repr():
    teacher = Teacher(id=1, user_id=3)
    assert repr(teacher) == '<Teacher 1>'

def test_teacher_grading_unassigned_assignment(client, h_teacher_2):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            'id': 1,  # Assignment assigned to teacher 1
            'grade': 'A'
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Only teacher who created the assignment can grade it'

def test_teacher_grading_invalid_state_assignment(client, h_teacher_1, h_student_1):
    # Create a new assignment in DRAFT state
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'Test Content'
        }
    )
    assignment_id = response.get_json()['data']['id']

    # Teacher tries to grade the DRAFT assignment
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            'id': assignment_id,
            'grade': 'A'
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Only submitted assignments can be graded'