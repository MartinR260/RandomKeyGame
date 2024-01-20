import unittest
from app import app, db, Leaderboard, SubmitScore

class TestRandomKeyCounter(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_submit_score(self):
        response = self.app.post('/submit_score', json={'username': 'test_user', 'score': 50})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Score submitted successfully')

    def test_leaderboard(self):
        response = self.app.get('/leaderboard')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1) 

if __name__ == '__main__':
    unittest.main()