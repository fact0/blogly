from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users class."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='')
        db.session.add(user)
        db.session.commit()

        self.assertEquals(user.full_name, "Michael Schienbein")

    def test_create_user(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='')
        db.session.add(user)
        db.session.commit()

        self.assertEquals(user.first_name, "Michael")
        self.assertEquals(user.last_name, "Schienbein")

    def test_edit_user(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='')
        db.session.add(user)
        db.session.commit()

        user.first_name = "Bob"
        user.last_name = "Bobberson"
        db.session.commit()

        self.assertEquals(user.first_name, "Bob")
        self.assertEquals(user.last_name, "Bobberson")

    def test_image_url(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='/static/blank.png')
        user2 = User(
            first_name='Greg',
            last_name='Abplanalp',
            image_url='www.testimage.com/image.png')
        self.assertEquals(user.image_url, '/static/blank.png')
        self.assertEquals(user2.image_url, 'www.testimage.com/image.png')
