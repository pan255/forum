from . import ModelMixin
from . import db
from . import timestamp


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    created_time = db.Column(db.Text, default=0)
    comments = db.relationship('Comment', backref="node")
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.node_id = form.get('node_id', '')
        self.user_id = form.get('user_id', '')
        self.created_time = timestamp()
        self.comments_num = 0
        self.last_comment_user = ''
        self.last_comment = ''


    def comments_num(self):
        self.comments_num = len(self.comments)
        if self.comments_num == 0:
            return None
        return self.comments_num

    def last_comment_user(self):
        if len(self.comments) == 0:
            return None
        return self.comments[-1].user

    def last_comment(self):
        if len(self.comments) == 0:
            return None
        return self.comments[-1]



