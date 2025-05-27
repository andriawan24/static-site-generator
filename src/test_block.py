import unittest

import blocks

class TestBlock(unittest.TestCase):
    def test_type_paragraph(self):
        block = "Test Normal Paragraph"
        block_type = blocks.block_to_block_type(block)
        self.assertEqual(block_type, blocks.BlockType.PARAGRAPH)

    def test_type_code(self):
        block = "```This is code```"
        block_type = blocks.block_to_block_type(block)
        self.assertEqual(block_type, blocks.BlockType.CODE)

    def test_type_code_invalid(self):
        block = "`This is code```"
        block_type = blocks.block_to_block_type(block)
        self.assertEqual(block_type, blocks.BlockType.PARAGRAPH)

    def test_type_ordered_list(self):
        block = "1. Test list ordered"
        block_type = blocks.block_to_block_type(block)
        self.assertEqual(block_type, blocks.BlockType.ORDERED_LIST)

    def test_type_ordered_list_invalid(self):
        block = "1.Test list ordered"
        block_type = blocks.block_to_block_type(block)
        self.assertEqual(block_type, blocks.BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """

        node = blocks.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = blocks.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()