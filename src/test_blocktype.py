import unittest


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        texts = [
            "# H1",
            "## H2",
            "### H3",
            "#### H4",
            "##### H5",
            "###### H6"
        ]
        for text in texts:
            actual = block_to_block_type(text)
            self.assertEqual(BlockType.Heading, actual)

    def test_faulty_heading(self):
        text = "#Hey"
        actual = block_to_block_type(text)
        self.assertEqual(BlockType.Paragraph, actual)

    def test_code(self):
        texts = [
            "```hi```",
            "```line1\nline2\nline3\n```",
        ]
        for text in texts:
            actual = block_to_block_type(text)
            self.assertEqual(BlockType.Code, actual)

    def test_faulty_code(self):
        text = "``````"
        actual = block_to_block_type(text)
        self.assertEqual(BlockType.Paragraph, actual)

    def test_quote(self):
        texts = [
            ">To Be or not To Be",
            ">Fuck\n>This\n>Shit",
        ]
        for text in texts:
            actual = block_to_block_type(text)
            self.assertEqual(BlockType.Quote, actual)

    def test_faulty_quote(self):
        text = ">Fuck\nThis"
        actual = block_to_block_type(text)
        self.assertEqual(BlockType.Paragraph, actual)

    def test_unordered_list(self):
        texts = [
            "- Item 1",
            "- Item 1\n- Item 2",
        ]
        for text in texts:
            actual = block_to_block_type(text)
            self.assertEqual(BlockType.UnorderedList, actual)

    def test_faulty_unordered_list(self):
        text = "- Item 1\n-Item 2"
        actual = block_to_block_type(text)
        self.assertEqual(BlockType.Paragraph, actual)

    def test_ordered_list(self):
        texts = [
            ". Item 1",
            ". Item 1\n. Item 2",
        ]
        for text in texts:
            actual = block_to_block_type(text)
            self.assertEqual(BlockType.OrderedList, actual)

    def test_faulty_ordered_list(self):
        text = ". Item 1\n.Item 2"
        actual = block_to_block_type(text)
        self.assertEqual(BlockType.Paragraph, actual)


if __name__ == '__main__':
    unittest.main()

from src.blocktype import block_to_block_type, BlockType
