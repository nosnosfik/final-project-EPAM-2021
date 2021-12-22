import os
import unittest
import department_app.views as views
from sqlalchemy.exc import IntegrityError
from datetime import date
from config import basedir, URL
from app import app, db
from department_app.models import Department, Employee


class ModelsFormsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_department(self):
        u = Department(name='dep1')
        expected = 'dep1'
        assert u.name == expected

    def test_make_department(self):
        u = Department(name='dep1')
        db.session.add(u)
        u2 = Department(name='dep2')
        db.session.add(u2)
        db.session.commit()
        departments = Department.query.all()
        assert len(departments) == 2

    def test_make_unique_department(self):
        u = Department(name='dep1')
        db.session.add(u)
        db.session.commit()
        u2 = Department(name='dep1')
        db.session.add(u2)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        all_departments = Department.query.all()
        assert len(all_departments) == 1

    def test_date_from_int(self):
        receive = views.date_from_int(108086400)
        excepted = '1973-06-05'
        assert excepted == str(receive)

    def test_date_to_int(self):
        receive = views.date_to_int(date.fromisoformat('1973-06-05'))
        excepted = 108086400
        assert receive == excepted

    def test_get_employees_avg_salary(self):
        u = Employee(employee_name='Vasyl', salary=10000, department_id=1,
                     date_of_birth=108086400)
        u2 = Employee(employee_name='Vasyl', salary=20000, department_id=1,
                      date_of_birth=108086400)
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        avg = views.get_employees_avg_salary(1)
        assert avg == 15000

    def test_404(self):
        tester = app.test_client(self)
        response = tester.get('/department',
                              follow_redirects=True)
        assert 404 == response.status_code

    def test_departments(self):
        tester = app.test_client(self)
        response = tester.get('/departments',
                              follow_redirects=True)
        assert 200 == response.status_code

    def test_new_departments(self):
        tester = app.test_client(self)
        response = tester.post('/new_department', data=dict(department_name="test"), follow_redirects=True)
        department = Department.query.all()
        assert 200 == response.status_code
        assert len(department) == 1
        assert department[0].name == 'test'

    def test_update_department(self):
        tester = app.test_client(self)
        u = Department(name='dep1')
        db.session.add(u)
        db.session.commit()
        response = tester.post('/departments/upd1', data=dict(department_name="test"), follow_redirects=True)
        department = Department.query.all()
        assert 200 == response.status_code
        assert len(department) == 1
        assert department[0].name == 'test'

    def test_delete_department(self):
        tester = app.test_client(self)
        u = Department(name='dep1')
        db.session.add(u)
        u2 = Department(name='dep2')
        db.session.add(u2)
        db.session.commit()
        response = tester.get('/departments/del2', follow_redirects=True)
        department = Department.query.all()
        assert 200 == response.status_code
        assert len(department) == 1


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        u = Department(name='dep1')
        db.session.add(u)
        u2 = Department(name='dep2')
        db.session.add(u2)
        u3 = Employee(employee_name='Vasyl', salary=10000, department_id=1,
                      date_of_birth=108086400)
        db.session.add(u3)
        u4 = Employee(employee_name='Methyl', salary=20000, department_id=1,
                      date_of_birth=108086400)
        db.session.add(u4)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_employee_get(self):
        response = self.app.get(f'{URL}/api/v1/employees', headers={"Content-Type": "application/json"})
        employee_name_got = response.json['employees'][1]['employee_name']
        employee_name_excepted = 'Methyl'
        assert response.status_code == 200
        self.assertEqual(employee_name_got, employee_name_excepted)

    def test_employee_get_direct(self):
        response = self.app.get(f'{URL}/api/v1/employee/2', headers={"Content-Type": "application/json"})
        employee_name_got = response.json['employee_name']
        employee_name_excepted = 'Methyl'
        assert response.status_code == 200
        self.assertEqual(employee_name_got, employee_name_excepted)

    def test_employee_post(self):
        self.app.post(f'{URL}/api/v1/new_employee', headers={"Content-Type": "application/json"},
                      json={'employee_name': 'Vasylec',
                            'salary': 10000,
                            'department_id': 1,
                            'date_of_birth': 108086400})
        response = self.app.get(f'{URL}/api/v1/employee/3', headers={"Content-Type": "application/json"})
        response_len = self.app.get(f'{URL}/api/v1/employees',
                                    headers={"Content-Type": "application/json"}).json['employees']
        employee_name_got = response.json['employee_name']
        employee_name_excepted = 'Vasylec'
        assert response.status_code == 200
        assert len(response_len) == 3
        self.assertEqual(employee_name_got, employee_name_excepted)

    def test_employee_patch(self):
        self.app.patch(f'{URL}/api/v1/employee/2', headers={"Content-Type": "application/json"},
                       json={'employee_name': 'Baranec'})
        response = self.app.get(f'{URL}/api/v1/employee/2', headers={"Content-Type": "application/json"})
        employee_name_got = response.json['employee_name']
        employee_name_excepted = 'Baranec'
        assert response.status_code == 200
        self.assertEqual(employee_name_got, employee_name_excepted)

    def test_employee_delete(self):
        response = self.app.delete(f'{URL}/api/v1/employee/del2', headers={"Content-Type": "application/json"})
        response_len = len(self.app.get(f'{URL}/api/v1/employees',
                                        headers={"Content-Type": "application/json"}).json['employees'])
        assert response.status_code == 200
        self.assertEqual(response_len, 1)


if __name__ == '__main__':
    unittest.main()
