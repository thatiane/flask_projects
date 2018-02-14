

from flask import send_from_directory
from python.database.create_tables import *

default_icon = Blueprint('default_icon', __name__)
app = Flask(__name__)

# website icon

@default_icon.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'admin.png', mimetype='image/vnd.microsoft.icon')

