import unittest

from flask import url_for

from todoism import create_app, db
from todoism.models import User, Item


class ToDoTestCase(unittst.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()

        user = User(username='yang')
        user.set_password('123')
        item1 = Item(body='Item 1', author=user)
        item2 = Item(body='Item 2', author=user)
        item3 = Item(body='Item 3', author=user)

        user2 = User(username='tao')
        user2.set_password('123')
        item = Item(body='Item', author=user2)

        db.session.add_all(user, item1, item2, item3, user2, item)
        db.session.commit()

        self.client.post(url_for('auth.login'), json=dict(username='yang', password='123'))

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_app_page(self):
        response = self.client.get(url_for('todo.app'))
        data = response.get_data(as_text=True)
        self.assertIn('What needs to be done?', data)
        self.assertIn('Clear', data)

    def test_new_item(self):
        response = self.client.post(url_for('todo.new_item'), json=dict(body='Item 4'))
        data = response.get_json()
        self.assertEqual(data['message'], '+1')
        self.assertIn('Item 4', data['html'])

        response = self.client.post(url_for('todo.new_item'), json=dict(body=' '))
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn(data['message'], 'Invalid item body.')

    def test_edit_item(self):
        response = self.client.put(url_for('todo.edit_item', item_id=1), json=dict(body='New Item 1'))
        data = response.get_json()
        self.assertEqual(Item.query.get(1).body, 'New Item 1')
        self.assertEqual(data['message'], 'Item updated.')

        response = self.client.put(url_for('todo.edit_item', item_id=1), json=dict(body=' '))
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Invalid item body.')

        response = self.client.put(url_for('todo.edit_item', item_id=4), json=dict(body='New Item B'))
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Permission denied.')

    def test_delete_item(self):
        response = self.client.delete(url_for('todo.delete_item', item_id=1))
        data = response.get_json()
        self.assertEqual(Item.query.get(1), None)
        self.assertEqual(data['message'], 'Item deleted.')

        response = self.client.delete(url_for('todo.delete_item', item_id=4))
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Permission denied.')

    def test_toggle_item(self):
        response = self.client.patch(url_for('todo.toggle_item', item_id=1))
        data = response.get_json()
        self.assertEqual(Item.query.get(1).done, True)
        self.assertEqual(data['message'], 'Item toggled.')

        response = self.client.patch(url_for('todo.toggle_item', item_id=1))
        data = response.get_json()
        self.assertEqual(Item.query.get(1).done, False)
        self.assertEqual(data['message'], 'Item toggled.')

        response = self.client.patch(url_for('todo.toggle_item', item_id=4))
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Permission denied.')

    def test_clear_item(self):
        self.client.patch(url_for('todo.toggle_item', item_id=1))
        self.client.patch(url_for('todo.toggle_item', item_id=2))

        response = self.client.delete(url_for('todo.clear_items'))
        data = response.get_json()
        self.assertEqual(data['message'], 'All clear!')
        self.assertEqual(Item.query.get(1), None)
        self.assertEqual(Item.query.get(2), None)
        self.assertNotEqual(Item.query.get(3), None)
