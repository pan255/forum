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
    return redirect(url_for('user.login'))


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


@main.route('/setting/avatar')
def setting_avatar():
    u = current_user()
    return render_template('user_setting_avatar.html', u=u)


@main.route('/upload', methods=['POST'])
def upload_file():
    u = current_user()
    uploads_dir = 'static/img/'
    f = request.files.get('uploaded')
    if f:
        filename = f.filename
        import uuid
        filename = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
        path = uploads_dir + filename
        f.save(path)
        u.upload_avatar(path)
    return redirect(url_for('user.setting_avatar'))


@main.route('/setting/password', methods=['POST'])
def setting_password():
    u = current_user()
    form = request.form
    u.change_password(form)
    return redirect(url_for('user.setting'))


@main.route('/setting/base_info', methods=['POST'])
def setting_base_info():
    u = current_user()
    form = request.form
    u.change_base_info(form)
    return redirect(url_for('user.setting'))