from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users class."""

    def setUp(self):
        """Clean up any existing users."""

        Post.query.delete()
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

        self.assertEqual(user.full_name, "Michael Schienbein")

    def test_create_user(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.first_name, "Michael")
        self.assertEqual(user.last_name, "Schienbein")

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

        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Bobberson")

    def test_image_url(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='https://files.catbox.moe/g1vsie.png')
        user2 = User(
            first_name='Greg',
            last_name='Abplanalp',
            image_url='www.testimage.com/image.png')
        self.assertEqual(
            user.image_url, 'https://files.catbox.moe/g1vsie.png')
        self.assertEqual(user2.image_url, 'www.testimage.com/image.png')


class PostModelTestCase(TestCase):
    """Tests for model for Users class."""

    def setUp(self):
        """Clean up any existing users."""

        Post.query.delete()
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_create_post(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='https://files.catbox.moe/g1vsie.png')
        post = Post(
            title='Test Post One',
            content='This is a models unittest post',
            user=user)
        db.session.add_all([user, post])
        db.session.commit()

        self.assertEqual(post.title, "Test Post One")
        self.assertEqual(post.content, "This is a models unittest post")

    def test_edit_post(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='https://files.catbox.moe/g1vsie.png')
        post = Post(
            title='Test Post One',
            content='This is a models unittest post',
            user=user)
        db.session.add_all([user, post])
        db.session.commit()

        post.title = "A New Title"
        post.content = "Some New Text"
        db.session.commit()

        self.assertEqual(post.title, "A New Title")
        self.assertEqual(post.content, "Some New Text")

    def test_db_relationship(self):
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='https://files.catbox.moe/g1vsie.png')
        post = Post(
            title='Test Post One',
            content='This is a models unittest post',
            user=user)
        db.session.add_all([user, post])
        db.session.commit()

        self.assertEqual(user.id, post.user_id)
        
