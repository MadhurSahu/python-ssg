import re
from enum import Enum


class BlockType(Enum):
    Heading = "heading"
    Paragraph = "paragraph"
    Code = "code"
    Quote = "quote"
    UnorderedList = "unordered_list"
    OrderedList = "ordered_list"


def block_to_block_type(block):
    if re.match(r"#{1,6} ", block):
        return BlockType.Heading
    if re.match(r"^```[\s\S]+```$", block):
        return BlockType.Code

    is_quote = True
    is_unordered_list = True
    is_ordered_list = True

    for line in block.split("\n"):
        if not is_quote and not is_unordered_list and not is_ordered_list:
            break
        if is_quote and not re.match(r"^>", line):
            is_quote = False
        if is_unordered_list and not re.match(r"^- ", line):
            is_unordered_list = False
        if is_ordered_list and not re.match(r"^\d+\. ", line):
            is_ordered_list = False

    if is_quote:
        return BlockType.Quote
    if is_unordered_list:
        return BlockType.UnorderedList
    if is_ordered_list:
        return BlockType.OrderedList
    return BlockType.Paragraph
