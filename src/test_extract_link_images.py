import unittest

import utils

class TestExtractLinkImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = utils.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_invalid_images(self):
         matches = utils.extract_markdown_images(
            "This is text with an ![[]i]m[age](https://i.imgur.com/zjjcJKZ.png)"
        )
         self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()