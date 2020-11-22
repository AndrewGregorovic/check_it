import random
import unittest

from flask_jwt_extended import create_access_token

from src.main import create_app, db
from src.models.Checklist import Checklist
from src.models.Item import Item
from src.models.User import User


class TestItems(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_item_create(self):
        checklist = random.choice(Checklist.query.all())
        user = User.query.get(checklist.owner_id)
        access_token = create_access_token(identity=str(user.id))

        response = self.client.post(f"/users/{user.id}/checklists/{checklist.id}/items/",
                                    json={
                                        "name": "test item",
                                        "index": random.randint(2, 10),
                                        "checklist_id": checklist.id
                                    }, headers={
                                        "Authorization": f"Bearer {access_token}"
                                    })

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertIn("id", data.keys())
        self.assertIsInstance(data["id"], int)
        self.assertIn("name", data.keys())
        self.assertIsInstance(data["name"], str)
        self.assertIn("status", data.keys())
        self.assertIsInstance(data["status"], bool)
        self.assertIn("index", data.keys())
        self.assertIsInstance(data["index"], int)
        self.assertIn("completion_date", data.keys())
        self.assertEqual(data["completion_date"], None)
        self.assertIn("assigned_id", data.keys())
        self.assertEqual(data["assigned_id"], None)
        self.assertIn("checklist_id", data.keys())
        self.assertEqual(data["checklist_id"], checklist.id)

        item = Item.query.get(data["id"])
        self.assertIsNotNone(item)

    def test_item_show(self):
        item = random.choice(Item.query.all())
        checklist = Checklist.query.get(item.checklist_id)
        user = User.query.get(checklist.owner_id)
        access_token = create_access_token(identity=str(user.id))

        response = self.client.get(f"/users/{user.id}/checklists/{checklist.id}/items/{item.id}",
                                   headers={
                                       "Authorization": f"Bearer {access_token}"
                                   })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 7)

    def test_item_update(self):
        item = random.choice(Item.query.all())
        checklist = Checklist.query.get(item.checklist_id)
        user = User.query.get(checklist.owner_id)
        access_token = create_access_token(identity=str(user.id))

        response = self.client.patch(f"/users/{user.id}/checklists/{checklist.id}/items/{item.id}",
                                     json={
                                         "name": "changed name",
                                         "index": random.randint(2, 10),
                                         "status": not item.status,
                                         "checklist_id": checklist.id
                                     }, headers={
                                         "Authorization": f"Bearer {access_token}"
                                     })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 7)
        self.assertEqual(data["name"], item.name)
        self.assertIsInstance(data["index"], int)
        if item.status:
            self.assertIsInstance(data["completion_date"], str)
        else:
            self.assertEqual(data["completion_date"], None)
        self.assertEqual(data["checklist_id"], item.checklist_id)

    def test_item_delete(self):
        item = random.choice(Item.query.all())
        checklist = Checklist.query.get(item.checklist_id)
        user = User.query.get(checklist.owner_id)
        access_token = create_access_token(identity=str(user.id))

        response = self.client.delete(f"/users/{user.id}/checklists/{checklist.id}/items/{item.id}",
                                      headers={
                                          "Authorization": f"Bearer {access_token}"
                                      })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], str)
        self.assertIsInstance(data[1], dict)
        self.assertFalse(Item.query.get(data[1]["id"]))
