from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Setting

bp = Blueprint('settings', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    setting = Setting.query.first()
    if not setting:
        setting = Setting(opening_cash=0.0, opening_online=0.0)
        db.session.add(setting)
        db.session.commit()
        
    if request.method == 'POST':
        setting.opening_cash = float(request.form.get('opening_cash', 0))
        setting.opening_online = float(request.form.get('opening_online', 0))
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('settings.index'))
        
    return render_template('settings/index.html', setting=setting)

@bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if current_user.password != current_password:
        flash('Incorrect current password.', 'error')
        return redirect(url_for('settings.index'))
        
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('settings.index'))
        
    current_user.password = new_password
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('settings.index'))
