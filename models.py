from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """"""
    # @classmethod
    # def get_by_species(cls, species):
    #     return cls.query.filter_by(species=species).all()

    # @classmethod
    # def get_all_hunger(cls):
    #     return cls.query.filter(Pet.hunger > 20).all()

    def __repr__(self):
        u = self
        return f"<User id={u.id} name={u.first_name} {u.last_name} Image Url={u.image_url}>"

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(100), nullable=False,
                          default='/static/blank.png')

    # def greet(self):
    #     return f'Hi I am {self.name} the {self.species}'

    # def feed(self, amt=20):
    #     """Update hunger based off of amount"""
    #     self.hunger -= amt
    #     self.hunger = max(self.hunger, 0)
