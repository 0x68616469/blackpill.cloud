from flask_login import UserMixin
from .extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_member = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    nip = db.relationship("Nip", backref="user", uselist=False)
    lnaddr = db.relationship("Lnaddr", backref="user", uselist=False)
    invoice = db.relationship("Invoice", backref="user", uselist=False)

    images = db.relationship("Image", backref="user", uselist=True)

    def __repr__(self):
        return f'<User "{self.username}">'

class Nip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    username = db.Column(db.String(50), nullable=True, unique=True)
    hex = db.Column(db.String(520), nullable=True, unique=False)

    def __repr__(self):
        return f'<Nip "{self.username}">'

class Lnaddr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    username = db.Column(db.String(50), nullable=True, unique=True)
    forward_to = db.Column(db.String(520), nullable=True, unique=False)

    def __repr__(self):
        return f'<Lnaddr "{self.username}">'

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    
    invoice = db.Column(db.String(520), nullable=True)
    verify_url = db.Column(db.String(520), nullable=True)

    def __repr__(self):
        return f'<Invoice "{self.user_id.username}">'


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)

    path = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_delete = db.Column(db.DateTime, nullable=True)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Image "{self.path}">'