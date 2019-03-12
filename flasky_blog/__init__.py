from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flasky_blog.config import Config


app = Flask(__name__)
app.config.from_object(Config)

app.debug = False   #设置为 True,激活 flask-debug-tool
 #不加python shell导入会报错
'''来源：https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-\
        disable-sqlalchemy-track-modifications
'''
db = SQLAlchemy()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message= '请您先登录，再访问该页面'

mail = Mail()

# from flasky_blog import routes



def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(Config)
        app.debug = False
        db.init_app(app)
        bcrypt.init_app(app)
        toolbar.init_app(app)
        login_manager.init_app(app)
        
        from flasky_blog.users.routes import users_bp
        from flasky_blog.posts.routes import posts_bp
        from flasky_blog.main.routes import main_bp
        app.register_blueprint(users_bp)
        app.register_blueprint(posts_bp)
        app.register_blueprint(main_bp)

        return app