To run on a PC, must be installed:
[Python 3.9](https://www.python.org/downloads/) or higher

#### Clone repository

git clone https://github.com/nosnosfik/final-project-EPAM-2021

#### Initial setup

+ Create a virtual environment and activate it
`python -m venv \path\to\create\new\virtual\environment`
`.\venv\Scripts\activate`

+ Install all required dependencies for application to work
`pip install -r requirements.txt`

+ Install all migrations
`flask db init`
`flask db migrate`
`flask db upgrade`

+ Run tests
  `python tests.py`

+ Run project
`flask run`