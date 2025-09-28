import unittest

from src.markdown_parser import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, \
    text_to_textnodes, markdown_to_blocks
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

    def test_images(self):
        node = TextNode(
            "This is text with an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.Text,
        )
        expected = [
            TextNode("This is text with an image ", TextType.Text),
            TextNode("obi wan", TextType.Image, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        actual = split_nodes_image([node])
        self.assertEqual(expected, actual)

    def test_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.Text,
        )
        expected = [
            TextNode("This is text with a link ", TextType.Text),
            TextNode("to boot dev", TextType.Link, "https://www.boot.dev"),
            TextNode(" and ", TextType.Text),
            TextNode("to youtube", TextType.Link, "https://www.youtube.com/@bootdotdev"),
        ]
        actual = split_nodes_link([node])
        self.assertEqual(expected, actual)

    def test_inline_complete(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.Text),
            TextNode("text", TextType.Bold),
            TextNode(" with an ", TextType.Text),
            TextNode("italic", TextType.Italic),
            TextNode(" word and a ", TextType.Text),
            TextNode("code block", TextType.Code),
            TextNode(" and an ", TextType.Text),
            TextNode("obi wan image", TextType.Image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.Text),
            TextNode("link", TextType.Link, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)

    def test_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        actual = markdown_to_blocks(md)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
