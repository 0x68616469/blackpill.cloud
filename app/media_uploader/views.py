from flask import Blueprint, flash, redirect, url_for, render_template, send_from_directory, request, current_app
from flask_login import login_required, current_user
import random, string, os

from ..extensions import db, settings
from ..models import Image
from ..forms import MediaForm

media_uploader = Blueprint("media_uploader", __name__)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Check if the file is in the allowed extensions list
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings["allowed_extensions"]


@media_uploader.route('/media', methods=['GET'])
@login_required
def media():
    if not current_user.is_member:
        flash("You need to become a member to upload medias.", "error")
        return redirect(url_for('membership.membership_page'))
    form = MediaForm()
    context = {
        "form":form,
    }
    return render_template('media_uploader/media.html', **context)

@media_uploader.route('/m/<string:path>', methods=['GET'])
def get_media(path):
    image = Image.query.filter_by(path=path).first()
    if image:
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], path)
    else:
        path = "404.png"
        return send_from_directory("static/src", path)

@media_uploader.route('/media/show/<string:path>', methods=['GET'])
@login_required
def view_media(path):
    image = Image.query.filter_by(path=path).first()
    if image:
        if image.user == current_user:
            image.size /= 1_000_000
            image.size = round(image.size, 2)
            context = {"image":image}
            return render_template('media_uploader/view_media.html', **context)
        else:
            path = "404.png"
            return send_from_directory("static/src/", path)
    else:
        path = "404.png"
        return send_from_directory("static/src/", path)

@media_uploader.route('/media/delete/<string:path>', methods=['GET'])
@login_required
def delete_media(path):
    image = Image.query.filter_by(path=path).first()
    if image:
        if image.user == current_user:
            os.remove(os.path.join(settings["UPLOAD_FOLDER"], image.path))
            db.session.delete(image)
            db.session.commit()
            flash("Image deleted.", "success")
            return redirect(url_for("dashboard.dashboard_edit"))
        else:
            flash("Unauthorized.", "error")
            return redirect(url_for("media_uploader.new_media")) 
    else:
        flash("Image not found.", "error")
        return redirect(url_for("media_uploader.new_media"))

@media_uploader.route('/media/new', methods=['POST'])
@login_required
def new_media():
    if not current_user.is_member:
        flash("You need to become a member to upload medias.", "error")
        return redirect(url_for('membership.membership_page'))

    if request.method == "POST":
        form = MediaForm()
        if form.validate_on_submit():

            file = form.image.data

            if file.filename == "":
                flash("No file found.", "error")
                return redirect(url_for("media_uploader.media"))
            
            if file and allowed_file(file.filename):
                path = get_random_string(settings["image_length"]) + "." + file.filename.rsplit('.', 1)[1].lower()
                while Image.query.filter_by(path=path).first():
                    path = get_random_string(settings["image_length"]) + "." + file.filename.rsplit('.', 1)[1].lower()

                file.save(os.path.join(settings["UPLOAD_FOLDER"], path))
                size = os.stat(os.path.join(settings["UPLOAD_FOLDER"], path)).st_size
                if size > settings["image_max_size"]:
                    flash("Image size too big.", "error")
                    os.remove(os.path.join(settings["UPLOAD_FOLDER"], path))
                    return redirect(url_for("media_uploader.media"))


                # REMOVE EXIF
                # with open(app.config['UPLOAD_FOLDER']+path, "rb") as file_with_exif:
                #     image_exif = Img(file_with_exif)
                
                # if image_exif.has_exif:
                #     image_exif.delete_all()

                #     with open(app.config['UPLOAD_FOLDER']+path, "wb") as file_without_exif:
                #         file_without_exif.write(image_exif.get_file())
                
                new_image = Image(user=current_user, path=path, size=size)
                db.session.add(new_image)
                db.session.commit()
                return redirect(url_for("media_uploader.view_media", path=path))
            else:
                flash("File not allowed.", "error")
                return redirect(url_for("media_uploader.media"))
            
        flash("Unknown error, try again later.", "error")
    return redirect(url_for("media_uploader.media"))