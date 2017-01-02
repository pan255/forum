from models.user import User
from routes import *


main = Blueprint('user', __name__)

Model = User


@main.route('/')
def login_view():
    ms = Model.query.all()
    return render_template('login_view.html', node_list=ms)


@main.route('/register')
def register():
    return render_template('user_register.html')


@main.route('/login')
def login():
    return render_template('user_login.html')


@main.route('/signup', methods=['POST'])
def signup():
    form = request.form
    m = Model(form)
    if m.valid():
        m.save()
        return redirect(url_for('.login'))
    return abort(404)


@main.route('/signin', methods=['POST'])
def signin():
    form = request.form
    m = Model(form)
    user = User.query.filter_by(username=m.username).first()
    if m.valid_login(user):
        session['user_id'] = user.id
        return redirect(url_for('home.home'))
    return abort(404)


@main.route('/profile/<int:id>')
def profile(id):
    u = current_user()
    u1 = User.query.get(id)
    topic_list = u1.topics
    for topic in topic_list:
        topic.comments_num = topic.comments_num()
        topic.last_comment_user = topic.last_comment_user()
    return render_template('user_profile.html', u=u, u1=u1, topic_list=topic_list)


@main.route('/setting')
def setting():
    u = current_user()
    return render_template('user_setting.html', u=u)


@main.route('/update', methods=['POST'])
def update():
    user = current_user()
    form = request.form
    u = User(form)
    if u.valid():
        user.update(u)
    return redirect(url_for('home.home'))

@main.route('/signout')
def signout():
    session.pop('user_id')
    return redirect(url_for('home.home'))

