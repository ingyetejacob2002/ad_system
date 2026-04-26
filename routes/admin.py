from flask import Blueprint, render_template, redirect
from models import db, Ad
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return "Access Denied"
    ads = Ad.query.filter_by(status='pending').all()
    return render_template('admin.html', ads=ads)

@admin.route('/approve/<int:id>')
@login_required
def approve(id):
    ad = Ad.query.get(id)
    ad.status = 'approved'
    db.session.commit()
    return redirect('/admin')
