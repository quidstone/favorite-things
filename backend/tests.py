import unittest
import json
from api import create_app
from api.models import db


class ItemModelTestCase(unittest.TestCase):
    item_id = 0

    def setUp(self):
        "set up test fixtures"
        print('### Setting up flask server ###')
        self.app = create_app('test')

        self.client = self.app.test_client()

    def test_item_creation(self):
        "testing item creation"
        item = {
            "title": "pizza",
            "description": "what a nice food, i really like pizza",
            "ranking": 20,
            "category_id": 2,
            "item_meta": {
                "kind": "cheesy,pepperoni",
                "place": "pizza-hut"
            }
        }
        res = self.client.post(
            "/item", data=json.dumps(item), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)

    def test_item_get(self):
        "testing item get"
        res = self.client.get("/item/7")
        self.assertEqual(res.status_code, 200)

    def test_item_update(self):
        "testing item update"
        item = {
            "title": "LA",
            "description": "what a nice food, i really like pizza",
            "ranking": 20,
            "category_id": 2,
            "item_meta": {
                "kind": "cheesy,pepperoni",
                "place": "pizza-hut"
            }
        }
        res = self.client.put(
            "/item/7", data=json.dumps(item), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)

    def test_item_deletion(self):
        "testing item deletion"
        res = self.client.delete("/item/7")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
