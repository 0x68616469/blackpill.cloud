from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Nip, Lnaddr
from ..forms import NipForm, LnaddrForwardForm

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard.route('/', methods=['GET'])
@login_required
def dashboard_page():
    if not current_user.is_member:
        flash("You need to become a member to access your dashboard.", "error")
        return redirect(url_for('membership.membership_page'))
    
    context = {
        "images":current_user.images,
    }

    return render_template('dashboard/dashboard.html', **context)

@dashboard.route('/edit', methods=['GET'])
@login_required
def dashboard_edit():
    if not current_user.is_member:
        flash("You need to become a member to access your dashboard.", "error")
        return redirect(url_for('membership.membership_page'))
    
    nip_form = NipForm()
    lnaddr_form = LnaddrForwardForm()

    if current_user.nip:
        if current_user.nip.username:
            nip_form.username.data = current_user.nip.username
        if current_user.nip.hex:
            nip_form.hex.data = current_user.nip.hex

    if current_user.lnaddr:
        if current_user.lnaddr.username: 
            lnaddr_form.username.data = current_user.lnaddr.username
        if current_user.lnaddr.forward_to: 
            lnaddr_form.forward_to.data = current_user.lnaddr.forward_to

    context = {
        "lnaddr_form":lnaddr_form,
        "nip_form":nip_form,
        "images":current_user.images,
    }

    return render_template('dashboard/dashboard_edit.html', **context)

@dashboard.route('/nip', methods=['POST'])
@login_required
def change_nip():
    if not current_user.is_member:
        flash("You need to become a member to change your NIP-05.", "error")
        return redirect(url_for('membership.membership_page'))
    
    nip_form = NipForm()

    if nip_form.is_submitted():
        if nip_form.validate():
            nip_username = nip_form.username.data
            if not nip_username.isalnum():
                flash("Only alphanumeric characters are allowed in the NIP-05 username.", "error")
                return redirect(url_for('dashboard.dashboard_edit'))
            if Nip.query.filter_by(user=current_user).first():
                Nip.query.filter_by(user=current_user).delete()
            new_nip = Nip(user=current_user, username=nip_username, hex=nip_form.hex.data)
            db.session.add(new_nip)
            db.session.commit()
            flash("NIP-05 successfully saved.", "success")
        else:
            flash("That NIP-05 username already exists. Please choose a different one.", "warning")
    
    return redirect(url_for('dashboard.dashboard_page'))

@dashboard.route('/lnaddr', methods=['POST'])
@login_required
def change_lnaddr():
    if not current_user.is_member:
        flash("You need to become a member to change your lightning address.", "error")
        return redirect(url_for('membership.membership_page'))
    
    lnaddr_form = LnaddrForwardForm()

    if lnaddr_form.is_submitted():
        if lnaddr_form.validate():
            lnaddr_username = lnaddr_form.username.data
            if not lnaddr_username.isalnum():
                flash("Only alphanumeric characters are allowed in the lightning address username.", "error")
                return redirect(url_for('dashboard.dashboard_edit'))
            if Lnaddr.query.filter_by(user=current_user).first():
                Lnaddr.query.filter_by(user=current_user).delete()
            new_lnaddr = Lnaddr(user=current_user, username=lnaddr_username, forward_to=lnaddr_form.forward_to.data)
            db.session.add(new_lnaddr)
            db.session.commit()
            flash("Lightning Address successfully saved.", "success")
        else:
            flash("That lightning address username already exists. Please choose a different one.", "warning")

    return redirect(url_for('dashboard.dashboard_page'))