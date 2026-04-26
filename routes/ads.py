from flask import Blueprint, render_template, request, redirect
from models import db, Ad, Click
from flask_login import login_required, current_user
import os

ads = Blueprint('ads', __name__)

@ads.route('/')
def home():
    ads_list = Ad.query.filter_by(status='approved').all()
    return render_template('index.html', ads=ads_list)

@ads.route('/dashboard')
@login_required
def dashboard():
    user_ads = Ad.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', ads=user_ads)

@ads.route('/create_ad', methods=['GET','POST'])
@login_required
def create_ad():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file.save(os.path.join('static/uploads', filename))

        ad = Ad(
            title=request.form['title'],
            link=request.form['link'],
            image=filename,
            user_id=current_user.id
        )
        db.session.add(ad)
        db.session.commit()
        return redirect('/dashboard')

    return render_template('create_ad.html')

@ads.route('/click/<int:id>')
def click(id):
    click = Click(ad_id=id)
    db.session.add(click)
    db.session.commit()

    ad = Ad.query.get(id)
    return redirect(ad.link)
