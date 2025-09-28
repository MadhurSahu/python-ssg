from enum import Enum

from src.leafnode import LeafNode


class TextType(Enum):
    Text = "text"
    Bold = "bold"
    Italic = "italic"
    Code = "code"
    Link = "link"
    Image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html(self):
        match self.text_type:
            case TextType.Text:
                return LeafNode(None, self.text)
            case TextType.Bold:
                return LeafNode("b", self.text)
            case TextType.Italic:
                return LeafNode("i", self.text)
            case TextType.Code:
                return LeafNode("code", self.text)
            case TextType.Link:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.Image:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError("Invalid text type")
