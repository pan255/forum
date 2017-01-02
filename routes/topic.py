from models.topic import Topic
from routes import *


main = Blueprint('topic', __name__)

Model = Topic


@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('topic_index.html', topic_list=ms)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.save()
    node_id = m.node_id
    return redirect(url_for('node.show', id=node_id))


@main.route('/<int:id>')
def show(id):
    u = current_user()
    m = Model.query.get(id)
    m.comments_num = m.comments_num()
    m.last_comment = m.last_comment()
    return render_template('topic.html', topic=m, u=u)


@main.route('/delete/<int:id>')
def delete(id):
    m = Model.query.get(id)
    m.delete()
    return redirect(url_for('.index'))


@main.route('/new/<int:id>')
def new(id):
    u = current_user()
    if u is not None:
        return render_template('topic_new.html', node_id=id, u=u)
    return render_template('register_or_login.html')