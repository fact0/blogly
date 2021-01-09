from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
DEFAULT_IMAGE = '/static/blank.png'

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def render_user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)


@app.route('/users/new')
def render_new_user_page():

    return render_template('newuser.html')


@app.route('/users/new', methods=['POST'])
def create_new_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def render_user_details(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user, default=DEFAULT_IMAGE)


@app.route('/users/<int:user_id>/edit')
def render_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edituser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name if first_name else user.first_name
    user.last_name = last_name if last_name else user.last_name
    user.image_url = image_url if image_url else user.image_url
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(f'/users')
