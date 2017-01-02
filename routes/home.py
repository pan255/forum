from models.node import Node
from models.topic import Topic
from routes import *


main = Blueprint('home', __name__)


@main.route('/')
def home():
    u = current_user()
    node_list = Node.query.all()
    topic_list = Topic.query.all()
    for topic in topic_list:
        topic.comments_num = topic.comments_num()
        topic.last_comment_user = topic.last_comment_user()
    return render_template('home.html', node_list=node_list, topic_list=topic_list, u=u,)
