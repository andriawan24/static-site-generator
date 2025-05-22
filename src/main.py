from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode

def text_node_to_html_code(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return ParentNode(tag="a", children=[LeafNode(value=text_node.text)], props={"href": text_node.url, "target": "_blank"})
        case TextType.IMAGE:
            return ParentNode(tag="img", children=[LeafNode(value="")], props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("The tag is currently unsupported")

def main():
    node = TextNode(text="This is a image", text_type=TextType.IMAGE, url="https://google.com")
    print(text_node_to_html_code(node).to_html())

main()