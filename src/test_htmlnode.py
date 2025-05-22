import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_html_without_props(self):
        node = HTMLNode(tag="h1", value="Test Value", children=[HTMLNode(tag="p", value="Test P Value")])
        self.assertEqual(node.tag, "h1")

    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Test Link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_html_prop_none(self):
        node = HTMLNode(tag="p", value="Test Paragraph")
        self.assertEqual(node.children, None)

if __name__ == '__main__':
    unittest.main()
