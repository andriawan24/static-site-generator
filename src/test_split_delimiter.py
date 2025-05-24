import unittest

from textnode import TextNode, TextType
import utils

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_code_type(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue(len(new_nodes) == 3)
        self.assertTrue(new_nodes[1].text_type, TextType.CODE)

    def test_invalid_node(self):
        node = TextNode("This is text with a `code block word", TextType.NORMAL)
        with self.assertRaises(ValueError) as context:
            _ = utils.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("invalid markdown, formatted not closed", context.exception)

if __name__ == "__init__":
    unittest.main()

