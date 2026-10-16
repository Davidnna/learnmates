import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class BasicSmokeTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite://")
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(User(name="Test Student", email="student@example.com",
                                password_hash=generate_password_hash("correct-horse-battery")))
            db.session.commit()
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="csrf_token"', response.data)

    def test_post_without_csrf_token_is_rejected(self):
        response = self.client.post("/login", data={"email": "student@example.com", "password": "wrong-password"})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
