from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from core.models.teachers import Teacher

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        include_fk = True