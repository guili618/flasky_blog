from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from forms import RegistrationForm,LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #不加python shell导入会报错
'''来源：https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-\
        disable-sqlalchemy-track-modifications
'''
db = SQLAlchemy(app)


from flasky_blog import routes