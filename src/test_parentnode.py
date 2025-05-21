import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nesting_parent(self):
        child_node = LeafNode("b", "Hello World")
        parent_node = ParentNode("p", children=[child_node])
        nested_parent_node = ParentNode("div", children=[parent_node])

        self.assertEqual(nested_parent_node.to_html(), "<div><p><b>Hello World</b></p></div>")

if __name__ == "__main__":
    unittest.main()