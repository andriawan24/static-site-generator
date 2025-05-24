from textnode import TextNode, TextType
import utils

def main():
    node = TextNode(text="This is a image", text_type=TextType.IMAGE, url="https://google.com")
    print(utils.text_node_to_html_code(node).to_html())

main()
