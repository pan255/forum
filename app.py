from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.user import User
from models.node import Node
from models.topic import Topic
from models.comment import Comment


app = Flask(__name__)
db_path = 'bbs.sqlite'
manager = Manager(app)


def register_routes(app):
    from routes.home import main as routes_home
    from routes.node import main as routes_node
    from routes.topic import main as routes_topic
    from routes.user import main as routes_user
    from routes.comment import main as routes_comment
    from routes.timeline import main as routes_timeline
    from routes.api import main as routes_api

    app.register_blueprint(routes_home)
    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_topic, url_prefix='/topic')
    app.register_blueprint(routes_comment, url_prefix='/comment')
    app.register_blueprint(routes_timeline, url_prefix='/timeline')
    app.register_blueprint(routes_api, url_prefix='/api')

def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/bbs'
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    # app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()

# gunicorn -b '0.0.0.0:80' redischat:app