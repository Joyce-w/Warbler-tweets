"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        # create user model 
        u1 = User(id=36, username='test1', email='test1@gmail.com', password='password1')
        db.session.add(u1)
        db.session.commit()

        self.u1_id = u1.id
        self.username = u1.username
        self.email = u1.email

        u2 = User(id=26, username='test2', email='test2@gmail.com', password='password2')
        db.session.add(u2)
        db.session.commit()

        self.u2_id = u2.id
        self.username = u2.username
        self.email = u2.email

        u3 = User(id=16, username='test3', email='test3@gmail.com', password='password3')
        db.session.add(u3)
        db.session.commit()

        self.u3_id = u3.id
        self.username = u3.username
        self.email = u3.email

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
    def test_dupe_model(self):
        """Check only 1 user registered if a duplicate user is given to signup"""

        dupe_u = User.signup(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD",
            image_url = None
        )

        db.session.add(dupe_u)
        db.session.commit()

        user = User.query.filter(User.username == 'testuser').all()
        self.assertEqual(len(user), 1)

    def test_login(self):
        """Test credentials if successful login provided"""
        user = User.authenticate('testuser', 'HASHED_PASSWORD')

        with self.client as c:
            resp = c.get("/")
            html = str(resp.data)

    def test_follwers(self):
        """Test followers/following"""

        f1 = Follows(user_being_followed_id=self.u1_id, user_following_id=self.u2_id)
        f2 = Follows(user_being_followed_id=self.u3_id, user_following_id=self.u2_id)

        db.session.add(f1)
        db.session.add(f2)
        db.session.commit()

        with self.client as c:
            followers = Follows.query.filter(Follows.user_following_id == self.u2_id).all()
            following = Follows.query.filter(Follows.user_being_followed_id == self.u2_id).all()

            self.assertEqual(len(followers), 2)
            self.assertEqual(len(following), 0)

