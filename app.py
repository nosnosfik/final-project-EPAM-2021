from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from auth_app.views import login_page_views
from department_app.views import department_views
from department_app.rest import rest


app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
import auth_app.models as models
# noinspection PyUnresolvedReferences
import department_app.models as department_models

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('logging.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

app.register_blueprint(department_views)
app.register_blueprint(login_page_views)
app.register_blueprint(rest)

login_manager = LoginManager()
login_manager.login_view = 'login_page_views.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/')
def index():  # put application's code here
    return render_template('auth_app/index.html', title='Home')


if __name__ == '__main__':
    app.run()
