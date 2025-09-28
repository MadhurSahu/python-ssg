import re

from src.textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            nodes.append(node)
            continue
        texts = node.text.split(delimiter)
        if len(texts) % 2 == 0:
            raise Exception(f"\"{node.text}\" has invalid markdown syntax")

        for i in range(len(texts)):
            if i % 2 == 0:
                nodes.append(TextNode(texts[i], TextType.Text))
            else:
                nodes.append(TextNode(texts[i], text_type))

    return nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)
