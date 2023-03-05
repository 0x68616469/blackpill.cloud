from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_required
import requests

from ..extensions import db, settings
from ..models import Invoice

membership = Blueprint("membership", __name__, url_prefix="/membership")

@membership.route('/', methods=['GET'])
@login_required
def membership_page():
    if current_user.is_member:
        flash("You're already a member.", "warning")
        return redirect(url_for('home.home_page'))
    
    
    if Invoice.query.filter_by(user=current_user).first():
        invoice = Invoice.query.filter_by(user=current_user).first().invoice
    else:
        alby_username = "blackpill"
        sat = settings["price"]
        milisat = sat * 1000
        comment = f"BlackPill membership for {current_user.username}"
        url = f"https://getalby.com/lnurlp/{alby_username}/callback?amount={milisat}&comment={comment}"

        try:
            r = requests.get(url)
            data = r.json()
        except:
            flash("Unknown error, try again later.", "error")
            return redirect(url_for("home.home_page"))

        if data['status'] == "OK":
            verify_url = data["verify"]
            invoice = data["pr"]
        else:
            flash("Unknown error, try again later.", "error")
            return redirect(url_for("home.home_page"))

        new_invoice = Invoice(user=current_user, verify_url=verify_url, invoice=invoice)
        db.session.add(new_invoice)
        db.session.commit()
    
    context = {
        "invoice":invoice,
    }
    return render_template('membership/membership.html', **context)

@membership.route('/check', methods=['GET'])
@login_required
def check_membership_invoice():
    if current_user.is_member:
        flash("You're already a member.", "warning")
        return redirect(url_for('home.home_page'))

    invoice = Invoice.query.filter_by(user=current_user).first()

    if not invoice:
        return redirect(url_for('membership.membership_page'))
    
    verify_url = invoice.verify_url
    try:
        r = requests.get(verify_url)
        data = r.json()
    except:
        flash("Unknown error, try again later.", "error")
        return redirect(url_for("home.home_page"))

    if data['status'] == "OK":
        if data["settled"] == True:
            Invoice.query.filter_by(user=current_user).delete()
            current_user.is_member = True
            db.session.commit()
            flash("You're now a member ! 🤙🏻", "success")
            return redirect(url_for('dashboard.dashboard_page'))
        else:
            flash("Invoice not payed yet, try again in few seconds.", "warning")
            return redirect(url_for('membership.membership_page'))
    else:
        flash("Unknown error, try again later.", "error")
        return redirect(url_for("home.home_page"))