from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')




@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #flash(f'账户已经为{form.username.data}创建!','success')
        flash(f'{form.username.data} 您好，账户已经为您创建', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'guili618@gmail.com':
            flash('您好，您已经成功登录', 'success')
            return redirect(url_for('home'))
        else:
            flash('请检查您的用户名和密码是否正确，谢谢！')
    return render_template('login.html',title='About',form=form)




if __name__ == '__main__':
    app.run(debug=True)



# POWERSHELL 
# $env:FLASK_APP = "flasky_blog.py"
# $env:FLASK_ENV = "development"