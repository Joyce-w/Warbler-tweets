"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"



# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

class UserAuthTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Add sample user models"""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

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
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        """Test user list"""
        with self.client as c:
            resp = c.get("/users")
            html = str(resp.data)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@test1", html)
            self.assertIn("@test3", html)          


    def test_dupe_user(self):
        with self.client as client:
            d={"username" :"test1", "email":"test1@gmail.com", "password": "password2"}
            resp = client.post('/signup', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="alert alert-danger">Username or email already taken</div>', html)

    def test_likes(self):
        # user doesnt exists??
        m = Message(id=1984, text="The earth is round", user_id=self.u1_id)
        db.session.add(m)
        db.session.commit()
        self.m_id = m.id

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u3_id

            res = c.post(f"/users/add_like/1984", follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            likes = Likes.query.filter(Likes.message_id==self.m_id).all()

            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.u3_id)

