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

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()



class MessageModelTestCase(TestCase):
    """Test models for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        # user model
        u1 = User(id = 8989,
                    username="testuser",
                    email="test@test.com",
                    password="testuser",
                    image_url=None)

        db.session.add(u1)
        db.session.commit()

        self.u1_id= u1.id

        # message model
        m = Message(
            id=1234,
            text="a test message",
            user_id=self.u1_id
        )
    
        db.session.add(m)
        db.session.commit()
        self.m1_id = m.id


        self.client = app.test_client()

    
    def test_message_delete(self):
        """Test whether message exists after delete"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post(f"/messages/{self.m1_id}/delete")

            msg = Message.query.filter(Message.id == self.m1_id).all()
            self.assertEqual(len(msg), 0)


    def test_message_model(self):
        """Test whether message exists after creation"""

        with self.client as c:
            msg = Message.query.filter(Message.id == self.m1_id).all()
            self.assertEqual(len(msg), 1)

