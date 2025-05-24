import unittest

from textnode import TextNode, TextType
import utils

class TestNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = utils.text_node_to_html_code(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = utils.text_node_to_html_code(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = utils.text_node_to_html_code(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")

    def test_code(self):
        node = TextNode("print('Hello World')", TextType.CODE)
        html_node = utils.text_node_to_html_code(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World')")
        self.assertEqual(html_node.to_html(), "<code>print('Hello World')</code>")

    def test_link(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="https://google.com")
        html_node = utils.text_node_to_html_code(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://google.com")
        self.assertEqual(html_node.to_html(), f"<a href=\"https://google.com\" target=\"_blank\">This is a link</a>")

    def test_image(self):
        node = TextNode(text="Image alt text", text_type=TextType.IMAGE, url="https://example.com/image.png")
        html_node = utils.text_node_to_html_code(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Image alt text")
        self.assertEqual(html_node.to_html(), f"<img src=\"https://example.com/image.png\" alt=\"Image alt text\"></img>")

if __name__ == "__main__":
    unittest.main()