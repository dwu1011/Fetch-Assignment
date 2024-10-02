import unittest
from flask import json
from app import app
from datetime import datetime, timezone


class PointsAPITestCase(unittest.TestCase):
    # Set up test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    # Test spending points
    def test_spend_points(self):
        self.app.post('/reset')

        self.app.post('/add', 
            data=json.dumps({
                "payer": "DANNON",
                "points": 5000,
                "timestamp": "2020-11-02T14:00:00Z"
            }),
            content_type='application/json')

        response = self.app.post('/spend', 
            data=json.dumps({
                "points": 3000
            }),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': -3000})

        response = self.app.get('/balance')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 2000})


    # Test adding points
    def test_add_points(self):
        self.app.post('/reset')

        response = self.app.post('/add', 
            data=json.dumps({
                "payer": "DANNON",
                "points": 5000,
                "timestamp": "2020-11-02T14:00:00Z"
            }),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/balance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 5000})


    def test_spend(self):
        # Add points
        self.app.post('/reset')

        self.app.post('/add', 
            data=json.dumps({
                "payer": "DANNON",
                "points": 300,
                "timestamp": "2022-10-31T10:00:00Z"
            }),
            content_type='application/json')
        
        response = self.app.get('/balance')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 300})

        self.app.post('/add', 
            data=json.dumps({
                "payer": "UNILEVER",
                "points": 200,
                "timestamp": "2022-10-31T11:00:00Z"
            }),
            content_type='application/json')
        
        response = self.app.get('/balance')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 300, 'UNILEVER': 200})

        self.app.post('/add', 
            data=json.dumps({
                "payer": "DANNON",
                "points": -200,
                "timestamp": "2022-10-31T15:00:00Z"
            }),
            content_type='application/json')
        
        response = self.app.get('/balance')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 100, 'UNILEVER': 200})

        self.app.post('/add', 
            data=json.dumps({
                "payer": "MILLER COORS",
                "points": 10000,
                "timestamp": "2022-11-01T14:00:00Z"
            }),
            content_type='application/json')

        response = self.app.get('/balance')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 100, 'UNILEVER': 200, 'MILLER COORS': 10000})

        self.app.post('/add', 
            data=json.dumps({
                "payer": "DANNON",
                "points": 1000,
                "timestamp": "2022-11-02T14:00:00Z"
            }),
            content_type='application/json')
        
        response = self.app.get('/balance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 1100, 'UNILEVER': 200, 'MILLER COORS': 10000})

        response = self.app.post('/spend', 
            data=json.dumps({
                "points": 5000
            }),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': -100, 'UNILEVER': -200, 'MILLER COORS': -4700})

        response = self.app.get('/balance')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'DANNON': 1000, 'UNILEVER': 0, 'MILLER COORS': 5300})


    # Test spending more points than available
    def test_spend_too_many_points(self):
        # Add points
        self.app.post('/add', 
            data=json.dumps({
                "payer": "DANNON",
                "points": 1000,
                "timestamp": "2020-11-02T14:00:00Z"
            }),
            content_type='application/json')

        response = self.app.post('/spend', 
            data=json.dumps({
                "points": 5000
            }),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("User doesn't have enough points", response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
