from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users class."""

    def setUp(self):
        """Clean up any existing users."""

        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

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

        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

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


class TagModelTestCase(TestCase):
    """Tests for model for Tag class."""

    def setUp(self):
        """Clean up any existing users."""

        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_create_tag(self):
        tag = Tag(
            name="Test")
        db.session.add(tag)
        db.session.commit()

        self.assertEqual(tag.id, 3)
        self.assertEqual(tag.name, "Test")


class PostTagModelTestCase(TestCase):
    """Tests for model for PostTag class."""

    def setUp(self):
        """Clean up any existing users."""

        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_db_relationship(self):
        tag1 = Tag(
            name="Test")
        tag2 = Tag(
            name="Test2")
        user = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='https://files.catbox.moe/g1vsie.png')
        post = Post(
            title='Test Post One',
            content='This is a models unittest post',
            user=user)
        db.session.add_all([user, post, tag1, tag2])
        db.session.commit()

        post_tag = PostTag(post_id=post.id, tag_id=tag2.id)
        db.session.add(post_tag)
        db.session.commit()

        self.assertEqual(tag1.id, 1)
        self.assertEqual(tag1.name, "Test")
        self.assertEqual(tag2.id, 2)
        self.assertEqual(tag2.name, "Test2")
        self.assertEqual(post.id, 4)
        self.assertEqual(post.title, "Test Post One")
        self.assertEqual(post_tag.post_id, 4)
        self.assertEqual(post_tag.tag_id, 2)
