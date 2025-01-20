import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from all_labs.lab_1.first_task import maximize_profit
from all_labs.lab_1.second_task import get_trends
import json
import unittest
from io import StringIO

class TestGetTrends(unittest.TestCase):

    def setUp(self):
        self.test_data = StringIO("""date,value
01.01.2020,10
02.01.2020,12
03.01.2020,15
04.01.2020,20
05.01.2020,25
""")

    def test_trends(self):
        result = get_trends(self.test_data)
        self.assertTrue(result["image_url"].startswith("data:image/png;base64,"))


class TestMaximizeProfit(unittest.TestCase):

    def setUp(self):
        self.json_data = json.dumps({
            "profit": [10, 20, 30],
            "time_matrix": [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ],
            "time_limits": [10, 20, 30],
            "products": ["product1", "product2", "product3"]
        })

    def test_maximize_profit(self):
        result = maximize_profit(self.json_data)
        
        result_json = json.loads(result)
        
        self.assertEqual(result_json["status"], 1)
        
        self.assertIn("product1", result_json["results"])
        self.assertIn("product2", result_json["results"])
        self.assertIn("product3", result_json["results"])

if __name__ == '__main__':
    unittest.main()