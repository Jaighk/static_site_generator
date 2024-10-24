import re
from textnode import *

def text_to_text_nodes(text: str) -> list:
    new_nodes = [TextNode(text, TextType.TEXT.value)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD.value)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC.value)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE.value)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT.value))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> list:
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text: str) -> list:
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links

def split_nodes_link(old_nodes: list) -> list:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT.value))
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed.")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT.value))
            new_nodes.append(TextNode(link[0], TextType.LINK.value, link[1]))
            original_text = sections[1]
        if original_text !="":
            new_nodes.append(TextNode(original_text, TextType.TEXT.value))
    return new_nodes

def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT.value))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE.value,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT.value))
    return new_nodes