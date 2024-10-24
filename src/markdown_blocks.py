from textnode import *
from htmlnode import * 
from inline_markdown import *
from enum import Enum 

class MdBlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"
    LINK = "link"
    IMAGE = "image"

MD_INDICATORS = {
    "#": MdBlockType.HEADING,
    "```": MdBlockType.CODE,
    ">": MdBlockType.QUOTE,
    "*": MdBlockType.ULIST,
    "1. ": MdBlockType.OLIST,
    "[": MdBlockType.LINK,
    "!": MdBlockType.IMAGE,
}

HTML_TAG = {
    "paragraph": "p",
    "heading": "h1", 
    "pre": "pre",
    "code": "code",
    "quote": "blockquote",
    "ordered_list": "ol",
    "unordered_list": "ul",
    "list_item": "li",
    "link": "a",
    "image": "img"
}

def markdown_to_block(markdown: str) -> list:
    blocks = []

    sections = markdown.split("\n\n")
    for section in sections:
        if section != "":
            blocks.append(section.strip())

    return blocks

def block_to_block_type(block: str) -> str:
    if block[:3] in MD_INDICATORS:
        if MD_INDICATORS[block[:3]] == MdBlockType.OLIST:
            block_components = block.split("\n")
            for component in block_components:
                block_components[block_components.index(component)] = component.strip()

            previous_num = 1

            for component in block_components:
                if block_components.index(component) == 0:
                    continue
                else:
                    if int(component[0]) != previous_num + 1:
                        raise ValueError(f"Block:\n\n{block}\n\nis not valid markdown")
                    previous_num = int(component[0])
            return MdBlockType.OLIST.value
        
        if MD_INDICATORS[block[:3]] == MdBlockType.CODE:
            if block[-3:] in MD_INDICATORS:
                return MdBlockType.CODE.value
            else:
                raise ValueError(f"Ivalid markdown: code block not closed")

    if block[0] in MD_INDICATORS:
        block_components = block.split("\n")

        for component in block_components:
            if component[0] != block_components[0][0]:
                raise ValueError(f"Block:\n{block}\nis not valid markdown")
        return MD_INDICATORS[block[0]].value

    return MdBlockType.PARAGRAPH.value

def markdown_to_htmlnode(text: str):
    new_htmlnodes = []
    # split markdown into blocks
    text_mdblocks = markdown_to_block(text)

    # loop over each block
    for block in text_mdblocks:
        # determine block_type
        block_type = block_to_block_type(block)
        block_text = block

        for indicator in MD_INDICATORS:
            block_text = block_text.strip().strip(indicator)

        if block_type == MdBlockType.ULIST.value or block_type == MdBlockType.OLIST.value or block_type == MdBlockType.QUOTE.value:
            list_items = block_text.split("\n")
            list_item_nodes = []
            for item in list_items: 
                for indicator in MD_INDICATORS:
                    item = item.strip().strip(indicator)
                new_htmlnode = HTMLNode("li", item)
                list_item_nodes.append(new_htmlnode)
            new_htmlnode = HTMLNode(HTML_TAG[block_type], None, list_item_nodes)
            new_htmlnodes.append(new_htmlnode)
        elif block_type == MdBlockType.CODE.value:
            code_node = HTMLNode(block_type, block_text)
            new_htmlnode = HTMLNode(HTML_TAG["pre"], None, code_node, None)
            new_htmlnodes.append(new_htmlnode)
        elif block_type == MdBlockType.LINK.value:
            link_component = block_text.split("(")
            block_text = link_component[0].strip("]")
            url = link_component[1].strip(")")
            new_htmlnode = HTMLNode(HTML_TAG[block_type], block_text, None, url)
            new_htmlnodes.append(new_htmlnode)
        elif block_type == MdBlockType.IMAGE.value:
            image_props = block_text.split("(")
            src = image_props[1].strip(")")
            alt = image_props[0].strip("[").strip("]")
            new_htmlnode = HTMLNode(block_type, alt, None, src)
            new_htmlnodes.append(new_htmlnode)
        else:
            new_htmlnode = HTMLNode(HTML_TAG[block_type], block_text)
            new_htmlnodes.append(new_htmlnode)
        
    # make all of the new HTMLNodes children to a single parent HMTMLNode (div) return it
    return ParentNode("div", new_htmlnodes)