"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

DEFAULT_IMAGE_URL = "https://th.bing.com/th/id/OIP.rFUJZbyB0YPChs_zA64VnwHaGj?w=209&h=185&c=7&r=0&o=5&pid=1.7"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(20),
                     nullable=False,
                     unique=False)

    last_name = db.Column(db.String(20),
                     nullable=False,
                     unique=False)

    image_url = db.Column(db.String(),
                    nullable=False, default= DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                     nullable=False,
                     unique=False)

    content = db.Column(db.Text,
                     nullable=False,
                     unique=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


