from . import ModelMixin
from . import db
from . import timestamp


class Timeline(db.Model, ModelMixin):
    __tablename__ = 'timelines'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_time = db.Column(db.Text, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get('content')
        self.created_time = timestamp()
        self.user_id = form.get('user_id')

    def update(self, form):
        self.content = form.get('content', '')
        self.save()