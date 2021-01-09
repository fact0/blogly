from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
DEFAULT_IMAGE = '/static/blank.png'


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

    @hybrid_property
    def full_name(self):
        """Returns full name of user"""
        return self.first_name + " " + self.last_name
