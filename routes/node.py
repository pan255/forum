from models.node import Node
from models.topic import Topic
from routes import *
from functools import wraps

main = Blueprint('node', __name__)

Model = Node


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u.id != 1:
            abort(404)
        return f(*args, **kwargs)
    return function


@main.route('/')
@admin_required
def index():
    ms = Model.query.all()
    return render_template('node_index.html', node_list=ms)


@main.route('/add', methods=['POST'])
@admin_required
def add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('.index'))


@main.route('/<int:id>')
def show(id):
    ms = Model.query.all()
    m = Model.query.get(id)
    u = current_user()
    topic_list = m.topics
    for topic in topic_list:
        topic.comments_num = topic.comments_num()
        topic.last_comment_user = topic.last_comment_user()
    return render_template('node.html', node=m, node_list=ms, u=u)


@main.route('/delete/<int:id>')
@admin_required
def delete(id):
    m = Model.query.get(id)
    m.delete()
    return redirect(url_for('.index'))
