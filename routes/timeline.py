from models.timeline import Timeline
from routes import *

# for decorators
from functools import wraps


main = Blueprint('timeline', __name__)

Model = Timeline


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u.id != 1:
            abort(404)
        return f(*args, **kwargs)
    return function


@main.route('/')
def index():
    u = current_user()
    ms = u.timelines
    return render_template('timeline_index.html', timeline_list=ms, u=u)


@main.route('/new')
def new():
    return render_template('timeline_new.html')


@main.route('/edit/<id>')
def edit(id):
    m = Model.query.get(id)
    return render_template('timeline_edit.html', timeline=m)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    m = Model.query.get(id)
    m.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
# @admin_required
def delete(id):
    m = Model.query.get(id)
    m.delete()
    return redirect(url_for('.index'))