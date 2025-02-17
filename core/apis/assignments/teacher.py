from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.apis.assignments.schema import AssignmentSchema, AssignmentGradeSchema
from core.libs import assertions

from .schema import AssignmentSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    assertions.assert_found(assignment, 'No assignment with this id was found')

    # Validation for draft state
    assertions.assert_valid(
        assignment.state == AssignmentStateEnum.SUBMITTED,
        'Only submitted assignments can be graded'
    )

    assertions.assert_valid(
        assignment.teacher_id == p.teacher_id,
        'Only teacher who created the assignment can grade it'
    )

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)