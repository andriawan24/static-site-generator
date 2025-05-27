from textnode import TextNode, TextType
import utils

def main():
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(utils.extract_markdown_links(text=text))

main()
