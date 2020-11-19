import random
import unittest

from src.main import create_app, db
from src.models.Checklist import Checklist
from src.models.Item import Item


class TestItems(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_item_create(self):
        checklist = random.choice(Checklist.query.all())
        response = self.client.post("/items/", json={
            "name": "test item",
            "index": random.randint(2, 10),
            "checklist_id": checklist.id
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue(bool("id" in data.keys()))
        
        item = Item.query.get(data["id"])
        self.assertIsNotNone(item)
        
    def test_item_show(self):
        checklist = random.choice(Checklist.query.all())
        response = self.client.get(f"/items/{checklist.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)

    def test_item_update(self):
        item = random.choice(Item.query.all())
        response = self.client.patch(f"/items/{item.id}", json={
            "name": "changed name",
            "index": random.randint(2, 10),
            "checklist_id": item.checklist_id
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "changed name")
        self.assertEqual(data["checklist_id"], item.checklist_id)

    def test_item_delete(self):
        item = random.choice(Item.query.all())
        response = self.client.delete(f"/items/{item.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], str)
        self.assertFalse(Item.query.get(data[1]["id"]))
