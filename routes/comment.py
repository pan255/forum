from models.comment import Comment
from routes import *


main = Blueprint('comment', __name__)

Model = Comment


@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('comment_index.html', comment_list=ms)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        form = request.form
        m = Model(form)
        m.save()
        topic_id = m.topic_id
        return redirect(url_for('topic.show', id=topic_id, u=u))
    return render_template('register_or_login.html')

# @main.route('/<int:id>')
# def show(id):
#     m = Model.query.get(id)
#     return render_template('topic.html', topic=m)


@main.route('/delete/<int:id>')
def delete(id):
    m = Model.query.get(id)
    m.delete()
    return redirect(url_for('.index'))