import bcrypt
import re

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column(db.String(100), nullable=False)  # Encrypted password field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    following = db.relationship('User', secondary='followers', 
                                primaryjoin=(id == 'followers.c.follower_id'),
                                secondaryjoin=(id == 'followers.c.followed_id'),
                                backref='followers')

    @property
    def password(self):
        """
        Getter for password.
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Setter for password. Automatically hashes the password.
        """
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        # Hash the password using bcrypt
        self._password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Check if the provided password matches the hashed password.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self._password.encode('utf-8'))

    @staticmethod
    def is_valid_email(email):
        """
        Validate email address format.
        """
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

    @staticmethod
    def is_valid_username(username):
        """
        Validate username format.
        """
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,50}$', username))

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    author = db.relationship('User', backref='blog_posts')

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)

    # Relationships
    author = db.relationship('User', backref='comments')
    post = db.relationship('BlogPost', backref='comments')
