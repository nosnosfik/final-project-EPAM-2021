from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Optional


class DepartmentForm(FlaskForm):
    department_name = StringField('department_name', validators=[DataRequired()])


class EmployeeForm(FlaskForm):
    employee_name = StringField('employee_name', validators=[DataRequired()])
    department_id = SelectField('department_id', coerce=int, default=None)
    salary = IntegerField('salary', validators=[Optional()])
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()])

