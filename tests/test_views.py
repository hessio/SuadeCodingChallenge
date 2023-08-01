# test_views.py

import unittest
from ..app import create_app


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_generate_report_data_with_invalid_date(self):
        # Test the '/report/<string:date>' view with a date too recent
        response = self.app.get('/report/2023-07-31')
        self.assertEqual(response.status_code, 400)

        # Test the '/report/<string:date>' view with a date too old
        response = self.app.get('/report/2003-07-31')
        self.assertEqual(response.status_code, 400)

        # Test the '/report/<string:date>' view with a random string
        response = self.app.get('/report/invalid-date')
        self.assertEqual(response.status_code, 400)

    def test_date_range_edge_cases(self):
        # Test the '/report/<string:date>' view with a valid date (edge case, first date in range)
        response = self.app.get('/report/2019-08-1')
        self.assertEqual(response.status_code, 200)

        # Test the '/report/<string:date>' view with a valid date (edge case, last date in range)
        response = self.app.get('/report/2019-09-29')
        self.assertEqual(response.status_code, 200)

    def test_generate_report_data_valid_date(self):
        # Test the 'generate_report_data' view with a valid date
        response = self.app.get('/report/2019-08-01')
        expected_data = {
            "commissions": {
                "order_avg": 2314804.1042387243,
                "promotions": {
                    "2": 188049.40000000002,
                    "5": 1085618.5
                },
                "total": 20833236.93814852
            },
            "customers": 9,
            "discount_rate_avg": 0.13145131216518063,
            "items": 2895,
            "orders": 9,
            "total_discount_amount": 15152814.736907512
        }
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data, expected_data)

    def test_generate_report_data_invalid_date(self):
        # Test the 'generate_report_data' view with an invalid date format
        response = self.app.get('/report/invalid-date-format')
        self.assertEqual(response.status_code, 400)
        error_data = response.get_json()
        self.assertIn('Invalid date: invalid-date-format, date must exist and between range 2019-08-01 and 2019-09-29.',
                      error_data['error'])

    def test_generate_report_data_nonexistent_date(self):
        # Test the 'generate_report_data' view with a date that does not exist in the data source
        response = self.app.get('/report/2023-08-01')
        self.assertEqual(response.status_code, 400)
        error_data = response.get_json()

        self.assertIn('Date out of range: 2023-08-01, date must be range 2019-08-01 and 2019-09-29.', error_data['error'])

    def test_generate_report_data_invalid_http_method(self):
        # Test the 'generate_report_data' view with an HTTP method other than GET
        response = self.app.post('/report/2023-07-31')
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()