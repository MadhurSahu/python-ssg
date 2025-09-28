import unittest

from src.leafnode import LeafNode


class MyTestCase(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "click", {"href": "https://google.com"})
        self.assertEqual(
            node.to_html(),
            "<a href=\"https://google.com\">click</a>"
        )

        node2 = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node2.to_html(),
            "<p>Hello, world!</p>"
        )


if __name__ == '__main__':
    unittest.main()
