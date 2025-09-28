from functools import reduce

from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes must have a tag")
        if not self.children:
            raise ValueError("Parent nodes must have children")
        props_html = self.props_to_html()
        child_html = reduce(
            lambda acc, child: acc + child.to_html(),
            self.children,
            ""
        )
        return f"<{self.tag}{props_html}>{child_html}</{self.tag}>"
