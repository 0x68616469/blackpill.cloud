from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, login_required, logout_user

from ..extensions import bcrypt, db
from ..forms import LoginForm, RegisterForm
from ..models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already authenticated.", "warning")
        return redirect(url_for('home.home_page'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Welcome back {user.username} ! 👋🏻", "success")
                if current_user.is_member:
                    return redirect(url_for('dashboard.dashboard_page'))
                return redirect(url_for('membership.membership_page'))
            
        flash("Fail : username or password incorrect.","error")
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Successfuly logged out.", "success")
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Already authenticated.", "warning")
        return redirect(url_for('home.home_page'))
    
    form = RegisterForm()

    if form.is_submitted():
        if form.validate():
            username = form.username.data
            if not username.isalnum():
                flash("Only alphanumeric characters are allowed in the username.", "error")
            else:
                hashed_password = bcrypt.generate_password_hash(form.password.data)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created ! You can now login.", "success")
                return redirect(url_for('auth.login'))
        else:
            for field, error in form.errors.items():
                flash(f"Error : {field} - {error}", "error")

    return render_template('auth/register.html', form=form)