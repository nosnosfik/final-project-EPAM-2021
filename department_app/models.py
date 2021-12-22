from app import db


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(20))
    date_of_birth = db.Column(db.Integer)
    salary = db.Column(db.Float)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='SET NULL'), nullable=True)
    department = db.relationship('Department', backref=db.backref('employee', passive_deletes=True))
