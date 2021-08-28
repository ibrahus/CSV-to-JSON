import unittest
import json
import io
from app import flask_app


class CSVtoJSONTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flask_app
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_csv_to_json(self):
        with open('csv_example.csv', 'rb') as file:
            data = {
                'file': file
            }
            res = self.client().get("/csv-to-json", data=data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.content_type, 'application/json')

    def test_upload_non_csv_failed(self):
        data = {
            'file': (io.BytesIO(b'my file contents'), 'test_file.txt'),
        }
        res = self.client().get("/csv-to-json", data=data)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.status_code, 415)

    def test_no_file_uploaded_failed(self):
        res = self.client().get("/csv-to-json")
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
