from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

db = SQLAlchemy()
DEFAULT_IMAGE = 'https://files.catbox.moe/g1vsie.png'


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site User class"""

    def __repr__(self):
        u = self
        return f"<User id={u.id} name={u.first_name} {u.last_name} Image Url={u.image_url}>"

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(100), nullable=False,
                          default=DEFAULT_IMAGE)

    posts = db.relationship("Post", backref="user",
                            lazy=True, cascade="all, delete-orphan")

    @hybrid_property
    def full_name(self):
        """Returns full name of user"""
        return self.first_name + " " + self.last_name


class Post(db.Model):
    """Site Post class"""

    def __repr__(self):
        p = self
        return f"< Post id = {p.id} Title = {p.title} Content = {p.content} Created = {p.created_at} User id = {p.user_id}>"

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)

    @hybrid_property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Site Tag class"""

    def __repr__(self):
        t = self
        return f"< Tag id = {t.id} Name = {t.name} >"

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )


class PostTag(db.Model):
    """Site Tag class"""

    def __repr__(self):
        pt = self
        return f"< Post id = {pt.post_id} Tag id = {pt.tag_id} >"
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
