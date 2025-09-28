from textnode import TextNode, TextType


def main():
    node = TextNode("Hello", TextType.Plain)
    print(node)


if __name__ == '__main__':
    main()
