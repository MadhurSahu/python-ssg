import unittest

from src.split_nodes_delimiter import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.Text)
        expected = [
            TextNode("This is text with a ", TextType.Text),
            TextNode("bolded phrase", TextType.Bold),
            TextNode(" in the middle", TextType.Text),
        ]
        actual = split_nodes_delimiter([node], "**", TextType.Bold)

        self.assertEqual(expected, actual)  # add assertion here

    def test_italic(self):
        node = TextNode("This is text with a `code block` word", TextType.Text)
        expected = [
            TextNode("This is text with a ", TextType.Text),
            TextNode("code block", TextType.Code),
            TextNode(" word", TextType.Text),
        ]
        actual = split_nodes_delimiter([node], "`", TextType.Code)

        self.assertEqual(expected, actual)  # add assertion here

    def test_malformed(self):
        node = TextNode("This is text with a **bolded phrase in the middle", TextType.Text)
        self.assertRaises(
            Exception,
            split_nodes_delimiter,
            old_nodes=[node],
            delimiter="**",
            text_type=TextType.Bold,
        )


if __name__ == '__main__':
    unittest.main()
