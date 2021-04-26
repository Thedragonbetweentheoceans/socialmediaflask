from db import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)
    mail = db.Column(db.Text, nullable = False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.LargeBinary(length=2048), nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, nullable=False,)
    post = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)

class PostUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Text, nullable=False)
    likeordislike = db.Column(db.Integer, nullable=False)
