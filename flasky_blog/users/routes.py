from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flasky_blog import db, bcrypt
from flasky_blog.models import User, Post
from flasky_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flasky_blog.users.utils import save_picture, send_reset_email



users_bp = Blueprint('users',__name__)

# from . import users_bp



@users_bp.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #flash(f'账户已经为{form.username.data}创建!','success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).\
                          decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,\
               password = hashed_password  )
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} 您好，账户已经为您创建', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='register',form=form)


@users_bp.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,\
                                                form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(\
                                                        url_for('main.home'))
            #return redirect(url_for('home'))
        else:
            flash('登录失败，请检查您的邮箱和密码是否正确，谢谢！','danger')
    return render_template('login.html',title='About',form=form)


@users_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users_bp.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('个人信息已成功更新!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email
    image_file = url_for('static',filename='images/' + current_user.image_file)
    return render_template('account.html',title='Account',\
                                        image_file=image_file,form=form)







@users_bp.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)






@users_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('重置密码的邮件已经发送到您的指定邮箱，请移步查看！', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', \
                            form=form)


@users_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).\
                                                        decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('您的密码已更新! 现在可以重新登录！！！', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='密码重置', form=form)