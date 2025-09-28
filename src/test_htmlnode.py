import unittest

from src.htmlnode import HTMLNode


class MyTestCase(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)


if __name__ == '__main__':
    unittest.main()
