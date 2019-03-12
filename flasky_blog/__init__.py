import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from forms import RegistrationForm,LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail

app = Flask(__name__)

app.debug = False   #设置为 True,激活 flask-debug-tool

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #不加python shell导入会报错
'''来源：https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-\
        disable-sqlalchemy-track-modifications
'''
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message= '请您先登录，再访问该页面'
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from flasky_blog import routes