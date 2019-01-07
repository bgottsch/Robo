from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
#from Robo.models import Post

settings = Blueprint('settings', __name__)

@settings.route("/settings")
def index():
    if current_user.is_authenticated:
        return render_template('settings.html')
    return redirect(url_for('users.login'))