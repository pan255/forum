from . import ModelMixin
from . import db
from . import timestamp
from models.user import User


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

    def get_avatar(self):
        u = User.query.get(self.user_id)
        return u.avatar

    def get_username(self):
        u = User.query.get(self.user_id)
        return u.username

    def update(self, form):
        self.content = form.get('content')
        self.save()

    def json(self):
        d = dict(
            id=self.id,
            content=self.content,
            created_time=self.created_time,
            user_id=self.user_id,
            avatar=self.get_avatar(),
            username=self.get_username(),
        )
        return d
