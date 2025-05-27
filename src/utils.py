import re

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

def text_node_to_html_node(text_node: TextNode):
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
        
def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result.append(node)
            continue

        current_text = node.text
        images = extract_markdown_images(current_text)

        if len(images) == 0:
            result.append(node)
            continue

        for image in images:
            sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Image is not closed")
            
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.NORMAL))

            result.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1]
                )
            )

            current_text = sections[1]
        
        if current_text != "":
            result.append(TextNode(current_text, TextType.NORMAL))

    return result

def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result.append(node)
            continue

        current_text = node.text
        links = extract_markdown_links(current_text)

        if len(links) == 0:
            result.append(node)
            continue

        for link in links:
            sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Image is not closed")
            
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.NORMAL))

            result.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1]
                )
            )

            current_text = sections[1]
        
        if current_text != "":
            result.append(TextNode(current_text, TextType.NORMAL))

    return result

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes