import unittest

import config


class TestCypher(unittest.TestCase):

    def setUp(self):
        self.message = 'Hello world'

    def test_encript(self):
        x = config.secret_encode(self.message)

    def test_decript(self):
        x = config.secret_encode(self.message)
        y = config.secret_decode(x)

    def test_cypher_revert(self):
        x = config.secret_encode(self.message)
        y = config.secret_decode(x)

        self.assertNotEqual(x, self.message)
        self.assertEqual(y, self.message)
