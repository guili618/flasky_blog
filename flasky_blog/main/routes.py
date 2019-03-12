from flask import render_template, request, Blueprint
from flasky_blog.models import Post

#from . import main_bp
main_bp = Blueprint('main', __name__)


@main_bp.route("/")
@main_bp.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc())\
                      .paginate(page=page,per_page=3)
    return render_template('home.html',posts=posts)

@main_bp.route("/about")
def about():
    return render_template('about.html',title='About')