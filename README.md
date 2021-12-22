# Application with REST API for departments, and theirs employees' management.

Database structure and all endpoints of the application are described below.

## Technical stack
+ Python version - 3.9
+ Main framework - Flask
+ Database - SQLite

## Main functionality
This project provides you to GET, POST, UPDATE and DELETE information about Departments and Employees.
And perform some sorting.


## Endpoint`s

### Departments:
```
+ GET /departments - a departments list
+ GET /departments/<department_id> - get information on a specific department
+ POST /new_department - create new department
+ PATCH /departments/upd<department_id> - update department's credentials
+ DELETE /departments/del<department_id> - delete department
```
### Employees:

```+ GET employees - employees list
+ GET /employee/<e_id> - obtaining information on a specific employee
+ POST /new_employee - create new employee
+ PATCH /employee/<e_id> - update employee's data
+ DELETE /employee/del<e_id> - delete employee by id
```


## API Endpoint`s

### Departments:
```
+ GET /api/v1/departments - a departments list in json format
+ GET /api/v1/departments/<department_id> - get information on a specific department in json format
+ POST /api/v1/new_department - create new department in json format
+ PATCH /api/v1/departments/upd<department_id> - update department's credentials in json format
+ DELETE /api/v1/departments/del<department_id> - delete department in json format
```
### Employees:

```+ GET /api/v1/employees - employees list in json format
+ GET /api/v1/employee/<e_id> - obtaining information on a specific employee in json format
+ POST /api/v1/new_employee - create new employee in json format
+ PATCH /api/v1/employee/<e_id> - update employee's data in json format
+ DELETE /api/v1/employee/del<e_id> - delete employee by id in json format
```