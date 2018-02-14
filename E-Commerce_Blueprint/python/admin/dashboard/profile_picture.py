
from flask import request
from shutil import rmtree
from werkzeug.utils import secure_filename
import os
from python.admin.login.login_check import *
from python.database.flask_database import *
profile = Blueprint('profile', __name__)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# upload admin profile picture

@profile.route('/admin/admin_profile_picture', methods=['post'])
@is_admin_logged_in
def admin_profile_picture():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(url_for('admin_dashboard'))
        file = request.files['file']
        if file.filename == '':
            flash('You Have to Select a File!', 'warning')
            return redirect(url_for('admin_dashboard'))
        if file and allowed_file(file.filename):
            try:
                rmtree(app.root_path + r"\static\uploads\users\{}".format(session['admin_username']))
                os.makedirs(app.root_path + r"\static\uploads\users\{}".format(session['admin_username']))
            except:
                os.makedirs(app.root_path + r"\static\uploads\users\{}".format(session['admin_username']))
            filename = secure_filename(file.filename)
            dir = app.root_path + r"\static\uploads\users\{}".format(session['admin_username'])
            file.save(os.path.join(dir, filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET files = %s WHERE username = %s AND permission = %s ;", [filename, session['admin_username'], session['permission']])
            mysql.connection.commit()
            cur.close()
            flash('You Have successfully uploaded Your Profile Picture!', 'success')
            return redirect(url_for('dashboard.admin_dashboard'))
    return redirect(url_for('dashboard.admin_dashboard'))