import re

from src.blocktype import block_to_block_type, BlockType
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.textnode import TextType, TextNode

REGEX_IMAGE = r"!\[([^\[\]]*)]\(([^()]*)\)"
REGEX_IMAGE_CAPTURE = r"(!\[[^\[\]]*]\([^()]*\))"
REGEX_LINK = r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)"
REGEX_LINK_CAPTURE = r"(?<!!)(\[[^\[\]]*]\([^()]*\))"


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        children.append(block_node)
    return ParentNode("div", children)


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


def block_to_html_node(block, block_type):
    if block_type == BlockType.Paragraph:
        return ParentNode("p", text_to_leaf_nodes(block.replace("\n", " ")))
    if block_type == BlockType.Heading:
        texts = re.split(r"^(#{1,6}) (.*)", block)
        return ParentNode(f"h{len(texts[0])}", text_to_leaf_nodes(texts[1]))
    if block_type == BlockType.Code:
        texts = re.findall(r"^```([\s\S]+)```$", block)
        code_block = LeafNode("code", texts[0].lstrip())
        return ParentNode("pre", [code_block])

    children = []
    for line in block.split("\n"):
        if block_type == BlockType.Quote:
            texts = re.findall(r"^>(.*)", line)
            children.extend(text_to_leaf_nodes(texts[0]))
            continue
        if block_type == BlockType.UnorderedList:
            texts = re.findall(r"^- (.*)", line)
            children.append(ParentNode("li", text_to_leaf_nodes(texts[0])))
            continue
        if block_type == BlockType.OrderedList:
            texts = re.findall(r"^\. (.*)", line)
            children.append(ParentNode("li", text_to_leaf_nodes(texts[0])))

    if block_type == BlockType.Quote:
        return ParentNode("blockquote", children)
    if block_type == BlockType.UnorderedList:
        return ParentNode("ul", children)
    if block_type == BlockType.OrderedList:
        return ParentNode("ol", children)

    raise ValueError(f"Unknown block type: {block_type}")


def text_to_leaf_nodes(text):
    return list(
        map(
            lambda text_node: text_node.to_html(),
            text_to_textnodes(text)
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
