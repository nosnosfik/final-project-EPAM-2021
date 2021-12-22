from flask import Blueprint, request, jsonify, make_response
from department_app.views import date_from_int, date_to_int, departments_name, get_employees_avg_salary

rest = Blueprint('rest', __name__, template_folder='templates')


def employee_data_to_dict(data):
    """Forming employee dictionary"""
    employee_data = {'id': data.id,
                     'employee_name': data.employee_name,
                     'date_of_birth': date_from_int(data.date_of_birth),
                     'salary': data.salary,
                     'department': departments_name(data.department_id)}
    return employee_data


def department_data_to_dict(data):
    """Forming department dictionary"""
    department_data = {'id': data.id,
                       'name': data.name}
    return department_data


@rest.route('/api/v1/employees', methods=['GET'])
def get_all_employees():
    """Employee api endpoint get list of all employees"""
    from department_app.models import Employee
    if not request.is_json:
        return make_response('No json for you today', 400)
    employees = Employee.query.all()
    output_json = []
    for employee in employees:
        output_json.append(employee_data_to_dict(employee))
    return jsonify({'employees': output_json})


@rest.route('/api/v1/employee/<e_id>', methods=['GET'])
def get_employee(e_id):
    """Employee api endpoint get employee by id"""
    from department_app.models import Employee
    if not request.is_json:
        return make_response('No json for you today', 400)
    employee = Employee.query.get_or_404(e_id)
    return jsonify(employee_data_to_dict(employee))


@rest.route('/api/v1/new_employee', methods=['POST'])
def post_employee():
    """Employee api endpoint to make new employee"""
    from app import db
    from department_app.models import Employee
    if not request.is_json:
        return make_response('No json for you today', 400)
    data = request.get_json()
    new_employee = Employee(employee_name=data['employee_name'],
                            date_of_birth=data['date_of_birth'],
                            salary=data['salary'],
                            department_id=data['department_id'],
                            )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'status': 'new employee has been created'})


@rest.route('/api/v1/employee/<e_id>', methods=['PATCH'])
def patch_employee(e_id):
    """Employee api endpoint to edit employee by id"""
    from app import db
    from department_app.models import Employee
    if not request.is_json:
        return make_response('No json for you today', 400)
    employee = Employee.query.get_or_404(e_id)
    data = request.get_json()
    if 'employee_name' in data:
        employee.employee_name = data['employee_name']
    if 'date_of_birth' in data:
        employee.date_of_birth = data['date_of_birth']
    if 'salary' in data:
        employee.salary = data['salary']
    if 'department_id' in data:
        employee.department_id = data['department_id']
    db.session.commit()
    return jsonify({'status': 'employee updated successfully'})


@rest.route('/api/v1/employee/del<e_id>', methods=['DELETE'])
def delete_employee(e_id):
    """Employee api endpoint to delete employee by id"""
    from app import db
    from department_app.models import Employee
    if not request.is_json:
        return make_response('No json for you today', 400)
    employee = Employee.query.get_or_404(e_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'status': 'employee deleted successfully'})


@rest.route('/api/v1/departments', methods=['GET'])
def get_all_departments():
    """Department api endpoint get list of all departments"""
    from department_app.models import Department
    if not request.is_json:
        return make_response('No json for you today', 400)
    departments = Department.query.all()
    output_json = []
    for department in departments:
        output_json.append(department_data_to_dict(department))
    return jsonify({'departments': output_json})


@rest.route('/api/v1/departments/<department_id>', methods=['GET'])
def get_department(department_id):
    """Department api endpoint get departments and it employees by id"""
    from department_app.models import Employee, Department
    if not request.is_json:
        return make_response('No json for you today', 400)
    department = Department.query.filter_by(id=department_id).get_or_404()
    employees = Employee.query.filter_by(department_id=department_id).all()
    to_json_employees = []
    for employee in employees:
        to_json_employees.append(employee_data_to_dict(employee))
    output_json = department_data_to_dict(department)
    output_json.update({'average salary': get_employees_avg_salary(department_id)})
    output_json.update({'employees': to_json_employees})
    return jsonify(output_json)


@rest.route('/api/v1/new_department', methods=['POST'])
def post_department():
    """Department api endpoint to make new department"""
    from app import db
    from department_app.models import Department
    if not request.is_json:
        return make_response('No json for you today', 400)
    data = request.get_json()
    new_department = Department(name=data['name'])
    db.session.add(new_department)
    db.session.commit()
    return jsonify({'status': 'new department has been created'})


@rest.route('/api/v1/departments/upd<department_id>', methods=['PATCH'])
def patch_department(department_id):
    """Department api endpoint to edit department by id"""
    from app import db
    from department_app.models import Department
    if not request.is_json:
        return make_response('No json for you today', 400)
    department = Department.query.get_or_404(department_id)
    data = request.get_json()
    if 'name' in data:
        department.employee_name = data['name']
    db.session.commit()
    return jsonify({'status': 'department updated successfully'})


@rest.route('/api/v1/departments/del<department_id>', methods=['DELETE'])
def delete_department(department_id):
    """Department api endpoint to delete department by id"""
    from app import db
    from department_app.models import Department
    if not request.is_json:
        return make_response('No json for you today', 400)
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    return jsonify({'status': 'department deleted successfully'})
