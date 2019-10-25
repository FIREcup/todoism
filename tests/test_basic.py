import unittest
from flask import current_app
from todoism import create_app
from todoism.extensions import db


class BasciTestCase(unittest.TestCase):
    def setUp(self):
        self.app =
