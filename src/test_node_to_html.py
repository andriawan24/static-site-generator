import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_code

# TODO: Add test cases
class TestNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_code(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_code(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://google.com")
        self.assertEqual(html_node.to_html(), f"<a href=\"https://google.com\" target=\"_blank\">This is a link</a>")