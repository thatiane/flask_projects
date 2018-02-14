

from flask import request
from werkzeug.utils import secure_filename
from shutil import rmtree
import os
from python.website.login.login_check import *
from python.database.flask_database import *

profile_picture_for_user = Blueprint('profile_picture_for_user', __name__)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# upload user profile picture

@profile_picture_for_user.route('/user_profile_picture', methods=['post'])
@is_user_logged_in
def user_profile_picture():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(url_for('account.user_account'))
        file = request.files['file']
        if file.filename == '':
            flash('You Have to Select a File!', 'warning')
            return redirect(url_for('account.user_account'))
        if file and allowed_file(file.filename):
            try:
                rmtree(app.root_path + r"\static\uploads\users\{}".format(session['user_username']))
                os.makedirs(app.root_path + r"\static\uploads\users\{}".format(session['user_username']))
            except:
                os.makedirs(app.root_path + r"\static\uploads\users\{}".format(session['user_username']))
            filename = secure_filename(file.filename)
            dir = app.root_path + r"\static\uploads\users\{}".format(session['user_username'])
            file.save(os.path.join(dir, filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET files = %s WHERE username = %s AND permission = %s;", [filename, session['user_username'], 'user'])
            mysql.connection.commit()
            cur.close()
            flash('You Have successfully uploaded Your Profile Picture!', 'success')
            return redirect(url_for('account.user_account'))
    return redirect(url_for('account.user_account'))
