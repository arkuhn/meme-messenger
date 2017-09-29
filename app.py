from flask import Flask, render_template, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
import blueprints.auth as auth

# start and configure app
app = Flask(__name__)
app.config.from_pyfile('app.cfg')


# register blueprints
app.register_blueprint(auth.auth)


# configure oauth with the client id, client secret, and server url
auth.configure_oauth(
    app.config['GOOGLE_OAUTH_CLIENTID'],
    app.config['GOOGLE_OAUTH_SECRET'],
    app.config['SERVER_NAME'])
db = SQLAlchemy(app)

# Database Models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# Routes


@app.route('/')
def main_page():
    """
    Loads main page
    """
    return render_template('base_page.html')


@app.route('/welcome')
def welcome_page():
    """
    Loads welcome page
    """
    return render_template('welcome.html')


@app.route('/account/<username>')
def account_page(username):
    """
    Loads account page
    """
    # See if this user is the user looking
    # Check to see if a user exists with that name
    existing_user = True
    user_data = {"username": username}
    if existing_user:
        # Temp List for now
        blocked = ['BigJim', 'Jerkface420', 'GuyFerrari']
        # Obtain the user's information somehow and package it in a dictionary
        user_data.update({"blocked_users": blocked, "privacy": 'friends'})
    return render_template(
        'account_page.html',
        user_data=user_data,
        existing_user=existing_user)


if __name__ == "__main__":
    app.run()
