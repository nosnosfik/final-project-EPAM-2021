from flask import render_template, Blueprint, redirect, url_for, request
from auth_app.service import login_required_admin
from datetime import date

department_views = Blueprint('department_views', __name__, template_folder='templates')


@department_views.errorhandler(404)
def not_found_error(error):
    """Renders 404 template if not found error raised"""
    return render_template('404.html'), 404


@department_views.errorhandler(500)
def internal_error(error):
    """Renders 500 template if not found error raised"""
    from app import db
    db.session.rollback()
    return render_template('500.html'), 500


def date_from_int(data):
    """Make date from timestamp"""
    return date.fromtimestamp(data)


def date_to_int(data):
    """Make timestamp from date"""
    return (data - date(1970, 1, 1)).total_seconds()


def get_employees_avg_salary(dep_id):
    """Gets all employees and calculates average salary"""
    from department_app.models import Employee
    avg_sal = 0
    d_employee = Employee.query.filter_by(department_id=dep_id).all()
    if d_employee:
        for emp in d_employee:
            avg_sal += emp.salary
        avg_sal /= len(d_employee)
        return round(avg_sal, 2)
    return 0


def departments_name(emp_id):
    """Get department name and shows it instead of id of department or 'Unemployed' status of employee"""
    from department_app.models import Department
    if emp_id is not 0:
        try:
            dep_name = Department.query.filter_by(id=emp_id).first().name
            return dep_name
        except AttributeError:
            return 'Unemployed'
    return 'Unemployed'


@department_views.route('/departments')
@login_required_admin
def departments():
    """Department endpoint get list of all departments"""
    from department_app.models import Department
    department = Department.query.all()
    return render_template('department_app/index.html', title="Departments", departments=department,
                           avg_sal=get_employees_avg_salary)


@department_views.route('/departments/<department_id>')
@login_required_admin
def department_by_id(department_id):
    """Department endpoint get department by id"""
    from department_app.models import Department, Employee
    department = Department.query.filter_by(id=department_id).first_or_404()
    d_employee = Employee.query.filter_by(department_id=department_id).all()
    return render_template('department_app/department.html', dfi=date_from_int, department=department,
                           employees=d_employee)


@department_views.route('/new_department', methods=['GET', 'POST'])
def new_department():
    """Department api endpoint to make new department"""
    from department_app.forms import DepartmentForm
    from department_app.models import Department
    from app import db
    form = DepartmentForm()
    if request.method == 'POST':
        department_name = form.department_name.data
        create_department = Department(name=department_name)
        db.session.add(create_department)
        db.session.commit()
        return redirect(url_for('department_views.departments'))
    return render_template('department_app/new_dep.html', form=form)


@department_views.route('/departments/upd<department_id>', methods=['GET', 'POST'])
def update_department(department_id):
    """Department api endpoint to edit department by id"""
    from department_app.forms import DepartmentForm
    from department_app.models import Department
    from app import db
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm()
    if request.method == 'POST':
        department.name = form.department_name.data
        db.session.commit()
        return redirect(url_for('department_views.departments'))
    form.department_name.data = department.name
    return render_template('department_app/dep_update.html', form=form)


@department_views.route('/departments/del<department_id>', methods=['GET'])
def delete_department(department_id):
    """Department endpoint to delete department by id"""
    from department_app.models import Department
    from app import db
    Department.query.filter_by(id=department_id).delete()
    db.session.commit()
    return redirect(url_for('department_views.departments'))


@department_views.route('/employees')
@login_required_admin
def employees():
    """Employee endpoint get list of all employees"""
    from department_app.models import Employee
    d_employee = Employee.query.all()
    return render_template('department_app/employees.html', title="Employees", employees=d_employee, dfi=date_from_int,
                           d_name=departments_name)


@department_views.route('/employee/<e_id>', methods=['GET', 'POST'])
def employee(e_id):
    """Employee endpoint to view or edit employee by id"""
    from department_app.forms import EmployeeForm
    from department_app.models import Employee, Department
    from app import db
    d_employee = Employee.query.get_or_404(e_id)
    form = EmployeeForm()
    available_groups = Department.query.all()
    groups_list = [(0, None)]
    groups_list.extend([(i.id, i.name) for i in available_groups])
    form.department_id.choices = groups_list
    if request.method == 'POST':
        d_employee.employee_name = form.employee_name.data
        d_employee.department_id = form.department_id.data
        d_employee.salary = int(form.salary.data)
        d_employee.date_of_birth = date_to_int(form.date_of_birth.data)
        db.session.commit()
        return redirect(url_for('department_views.employees'))
    form.employee_name.data = d_employee.employee_name
    form.salary.data = int(d_employee.salary)
    form.department_id.data = d_employee.department_id
    form.date_of_birth.data = date_from_int(d_employee.date_of_birth)
    return render_template('department_app/employee.html', dfi=date_from_int, form=form)


@department_views.route('/new_employee', methods=['GET', 'POST'])
def new_employee():
    """Employee endpoint to make new employee"""
    from department_app.forms import EmployeeForm
    from department_app.models import Employee, Department
    from app import db
    form = EmployeeForm()
    available_groups = Department.query.all()
    groups_list = [(0, None)]
    groups_list.extend([(i.id, i.name) for i in available_groups])
    form.department_id.choices = groups_list
    if request.method == 'POST':
        employee_name = form.employee_name.data
        salary = form.salary.data
        department_id = form.department_id.data
        date_of_birth = date_to_int(form.date_of_birth.data)
        create_employee = Employee(employee_name=employee_name, salary=salary, department_id=department_id,
                                   date_of_birth=date_of_birth)
        db.session.add(create_employee)
        db.session.commit()
        return redirect(url_for('department_views.employees'))
    return render_template('department_app/new_employee.html', form=form)


@department_views.route('/employee/del<e_id>', methods=['GET'])
def delete_employee(e_id):
    """Employee endpoint to delete employee by id"""
    from department_app.models import Employee
    from app import db
    Employee.query.filter_by(id=e_id).delete()
    db.session.commit()
    return redirect(url_for('department_views.employees'))

