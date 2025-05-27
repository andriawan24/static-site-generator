from enum import Enum

import re
import utils
from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        final_block = block.strip()
        filtered_blocks.append(final_block)
    return filtered_blocks


def block_to_block_type(text) -> BlockType:
    lines = text.split("\n")

    if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    elif text.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif text.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif len(re.findall(r"[0-9]*\. ", text)) > 0:
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    text_nodes = utils.text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = utils.text_node_to_html_node(text_node)
        children.append(html_node)
    return children
    
def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block == "":
            continue
        
        type = block_to_block_type(block)
        match (type):
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                paragraph = ' '.join([line.strip() for line in lines])
                children = text_to_children(paragraph)
                html_nodes.append(ParentNode("p", children))
            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break
                if level + 1 >= len(block):
                    raise ValueError(f"invalid level heading {level}")
                
                text = block[(level + 1):]
                children = text_to_children(text)
                html_nodes.append(ParentNode(f"h{level}", children))
            case BlockType.CODE:
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                text = block[4:-3]
                raw_text_node = TextNode(text, TextType.NORMAL)
                child = utils.text_node_to_html_node(raw_text_node)
                code = ParentNode("code", children=[child])
                html_nodes.append(ParentNode("pre", children=[code]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                children = text_to_children(content)
                html_nodes.append(ParentNode("blockquote", children))
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[3:]
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                html_nodes.append(ParentNode("ul", html_items))
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[2:]
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                html_nodes.append(ParentNode("ol", html_items))

    return ParentNode("div", html_nodes, None)
    
