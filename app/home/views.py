from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from ..models import User

home = Blueprint("home", __name__)

@home.route('/', methods=['GET'])
def home_page():
    return render_template('home/home.html')

@home.route('/rules', methods=['GET'])
def rules():
    return render_template('home/rules.html')

@home.route('/contact', methods=['GET'])
def contact():
    return render_template('home/contact.html')

@home.route('/key-converter', methods=['GET'])
@login_required
def key_converter():
    if not current_user.is_member:
        flash("You need to become a member to access the key converter.", "error")
        return redirect(url_for('membership.membership_page'))
    return render_template('home/keyconverter.html')

@home.route('/explore/<int:page>', methods=['GET'])
def explore_page(page):
    per_page = 10
    members = User.query.filter_by(is_member=True).order_by(User.id).paginate(page=page, per_page=per_page)
    total = int(User.query.filter_by(is_member=True).count() / per_page)
    if total == 0:
        total = 1
    context = {
        "members":members,
        "page":page,
        "total":total,
    }
    return render_template('home/explore.html', **context)


@home.route('/explore', methods=['GET'])
def explore():
    return redirect(url_for('home.explore_page', page=1))