from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))