from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
import os

from ..models import User, Image, Invoice, Nip, Lnaddr
from ..extensions import db, settings

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/stat", methods=["GET"])
@login_required
def stat():
    if not current_user.is_member:
        flash("You need to become an admin to access this page.", "error")
        return redirect(url_for("membership.membership_page"))
    
    if not current_user.is_admin:
        flash("You need to become an admin to access this page.", "error")
        return redirect(url_for("home.home_page"))      

    users = User.query.order_by(User.id).all()

    for user in users:
        user.number_of_image = len(user.images)
        user.size_of_images = 0
        for image in user.images:
            user.size_of_images += image.size
        user.size_of_images /= 1_000_000
        user.size_of_images = round(user.size_of_images, 2)

    context = {
        "users":users,
        "number_nip": Nip.query.count(),
        "number_user": User.query.count(),
        "number_member": User.query.filter_by(is_member=True).count(),
        "number_image": Image.query.count(),
        "number_invoice": Invoice.query.count(),
        "number_lnaddr": Lnaddr.query.count(),
    }

    return render_template("admin/stat.html", **context)


@admin.route("/delete/<string:username>", methods=["GET"])
@login_required
def admin_delete(username):
    if not current_user.is_member:
        flash("You need to become an admin to access this page.", "error")
        return redirect(url_for("membership.membership_page"))
    
    if not current_user.is_admin:
        flash("You need to become an admin to access this page.", "error")
        return redirect(url_for("home.home_page"))  

    user = User.query.filter_by(username=username).first()

    for image in user.images:
        os.remove(os.path.join(settings["UPLOAD_FOLDER"], image.path))
        db.session.delete(image)
    
    if user.invoice:
        db.session.delete(user.invoice)

    if user.nip:
        db.session.delete(user.nip)

    if user.lnaddr:
        db.session.delete(user.lnaddr)

    db.session.delete(user)
    flash("User deleted", "success")
    db.session.commit()

    return redirect(url_for("admin.stat"))  