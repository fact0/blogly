from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        u1 = User(
            first_name='Michael',
            last_name='Schienbein',
            image_url='/static/blank.png')
        u2 = User(
            first_name='Greg',
            last_name='Abplanalp',
            image_url='/static/blank.png')
        u3 = User(
            first_name='Ilya',
            last_name='Ornatov',
            image_url='/static/blank.png')
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        self.user_id = u1.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Michael Schienbein', html)
            self.assertIn('Greg Abplanalp', html)
            self.assertIn('Ilya Ornatov', html)

    def test_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "Bob", "last_name": "Bobberson",
                 "image_url": "/static/blank.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Bob Bobberson", html)

    def test_render_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Michael Schienbein', html)

    def test_render_user_edit(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-3">Edit a User:</h2>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Halim", "last_name": "Tannous",
                 "image_url": ""}
            resp = client.post(
                f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Halim Tannous", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotEqual('Michael Schienbein', html)
