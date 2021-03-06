from . import ModelMixin
from . import db
from . import timestamp

class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    comments = db.relationship('Comment', backref="user")
    avatar = db.Column(db.Text)
    email = db.Column(db.Text)
    company = db.Column(db.Text)
    website = db.Column(db.Text)
    created_time = db.Column(db.Text, default=0)
    topics = db.relationship('Topic', backref="user")
    timelines = db.relationship('Timeline', backref="user")

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', '/static/img/longmao.jpeg')
        self.created_time = timestamp()
        self.email = form.get('email', '')
        self.company = form.get('company', '')
        self.website = form.get('website', '')

    def valid_login(self, u):
        if u is not None:
            username_equals = u.username == self.username
            password_equals = u.password == self.password
            return username_equals and password_equals
        else:
            return False

    # 验证注册用户的合法性的
    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def update(self, u):
        self.password = u.password
        self.avatar = u.avatar
        self.save()

    def upload_avatar(self, path):
        self.avatar = '/' + path
        self.save()

    def change_password(self, form):
        if self.password == form['old_password']:
            if form['new_password'] == form['commit_password']:
                self.password = form['new_password']
                self.save()

    def change_base_info(self, form):
        self.email = form.get('email', '')
        self.company = form.get('company', '')
        self.website = form.get('website', '')
        self.save()
