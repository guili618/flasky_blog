from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField \
     ,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flasky_blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('用户名',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('邮箱',
                            validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired()])
    confirm_password =  PasswordField('确认密码',
                            validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已经被使用，请输入不同的用户名 ！')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该email已经被使用，请输入不同的email ！')

class LoginForm(FlaskForm):

    email = StringField('Email',
                            validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('用户名',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('邮箱',
                            validators=[DataRequired(),Email()])
    picture = FileField('修改头像',validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('更新个人信息')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('该用户名已经被使用，请输入不同的用户名 ！')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('该email已经被使用，请输入不同的email ！')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')