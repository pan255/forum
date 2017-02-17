from models.comment import Comment
from models.timeline import Timeline
from routes import *
import json

main = Blueprint('api', __name__)


@main.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()
    if u is not None:
        form = request.form
        c = Comment(form)
        c.save()
        d = c.json()
        return json.dumps(d)
    return None


@main.route('/timeline/add', methods=['POST'])
def timeline_add():
    form = request.form
    t = Timeline(form)
    t.save()
    d = t.json()
    return json.dumps(d)


@main.route('/timeline/delete/<int:id>')
def timeline_delete(id):
    print(id)
    t = Timeline.query.get(id)
    t.delete()
    d = t.json()
    return json.dumps(d)


@main.route('/timeline/edit/<int:id>', methods=['POST'])
def timeline_edit(id):
    form = request.form
    t = Timeline.query.get(id)
    t.update(form)
    d = t.json()
    return json.dumps(d)