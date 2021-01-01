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

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def render_user_list():
    users = User.query.all()

    return render_template('users.html', users=users)


@app.route('/users/new')
def render_new_user_page():

    return render_template('newuser.html')


@app.route('/users/new', methods=['POST'])
def create_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def render_user_details(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def render_user_edit(user_id):
    user = User.query.get(user_id)
    return render_template('edituser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    # user = User.query.get_or_404(user_id)

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):

    User.query.filter(User.id == user_id).delete()

    db.session.commit()

    # user = User.query.get_or_404(user_id)

    return redirect(f'/users')
