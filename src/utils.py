from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        nodes = []
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError("invalid markdown, formatted not closed")

        for i in range(len(splitted)):
            if splitted[i] == "":
                continue
            
            if i % 2 == 0:
                nodes.append(TextNode(splitted[i], TextType.NORMAL))
            else:
                nodes.append(TextNode(splitted[i], text_type))

        new_nodes.extend(nodes)

    return new_nodes


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