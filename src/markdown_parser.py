import re

from src.textnode import TextType, TextNode

REGEX_IMAGE = r"!\[([^\[\]]*)]\(([^()]*)\)"
REGEX_IMAGE_CAPTURE = r"(!\[[^\[\]]*]\([^()]*\))"
REGEX_LINK = r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)"
REGEX_LINK_CAPTURE = r"(?<!!)(\[[^\[\]]*]\([^()]*\))"


def markdown_to_blocks(markdown):
    return list(
        filter(
            lambda block: block != "",
            list(
                map(
                    lambda block: block.strip(),
                    markdown.split("\n\n")
                )
            )
        )
    )


def text_to_textnodes(text):
    node = TextNode(text, TextType.Text)
    nodes = split_nodes_delimiter([node], "**", TextType.Bold)
    nodes = split_nodes_delimiter(nodes, "_", TextType.Italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.Code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


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


def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            nodes.append(node)
            continue

        texts = re.split(REGEX_IMAGE_CAPTURE, node.text)
        for text in texts:
            if not text:
                continue

            parsed = re.match(REGEX_IMAGE, text)
            if parsed:
                image = parsed.groups()
                nodes.append(TextNode(image[0], TextType.Image, image[1]))
            else:
                nodes.append(TextNode(text, TextType.Text))
    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            nodes.append(node)
            continue

        texts = re.split(REGEX_LINK_CAPTURE, node.text)
        for text in texts:
            if not text:
                continue

            parsed = re.match(REGEX_LINK, text)
            if parsed:
                link = parsed.groups()
                nodes.append(TextNode(link[0], TextType.Link, link[1]))
            else:
                nodes.append(TextNode(text, TextType.Text))
    return nodes


def extract_markdown_images(text):
    return re.findall(REGEX_IMAGE, text)


def extract_markdown_links(text):
    return re.findall(REGEX_LINK, text)
