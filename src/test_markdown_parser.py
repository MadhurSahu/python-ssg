import unittest

from src.markdown_parser import split_nodes_delimiter, extract_markdown_images
from src.textnode import TextNode, TextType


class TestMarkdownParser(unittest.TestCase):
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

    def test_extract_markdown_links(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == '__main__':
    unittest.main()
