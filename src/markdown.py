from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
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
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == text_type_image:
            new_nodes.append(node)
            continue

        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue


        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(TextNode(node.text, text_type_text))
            continue

        sections = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)

        for section in sections:
            if section == "":
                continue

            section_links = extract_markdown_links(section)

            if len(section_links) == 0:
                new_nodes.append(TextNode(section, text_type_text))
                new_nodes.append(TextNode(links[0][0], text_type_link, links[0][1]))

            if len(section_links) != 0:
                new_nodes.extend(split_nodes_link([TextNode(section, text_type_text)]))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue

        sections = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)

        for section in sections:
            if section == "":
                continue

            section_images = extract_markdown_images(section)

            if len(section_images) == 0:
                if sections.index(section) % 2 == 0:
                    new_nodes.append(TextNode(section, text_type_text))
                    new_nodes.append(TextNode(images[0][0], text_type_image, images[0][1]))
                if sections.index(section) % 2 == 1:
                    new_nodes.append(TextNode(section, text_type_text))

            if len(section_images) != 0:
                new_nodes.extend(split_nodes_image([TextNode(section, text_type_text)]))

    return new_nodes

def text_to_text_nodes(text):
    new_nodes = [TextNode(text, text_type_text)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type_code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes

def markdown_to_block(markdown: str) -> list:
    blocks = []

    sections = markdown.split("\n\n")
    for section in sections:
        if section != "":
            blocks.append(section.strip())

    return blocks

def block_to_block_type(block: str) -> str:
    markdown_indicators = {
        "#": "heading",
        "```": "code",
        ">": "quote",
        "*": "unordered_list",
        "1. ": "ordered_list"}

    if block[:3] in markdown_indicators:
        if markdown_indicators[block[:3]] == "ordered_list":
            block_components = block.split("\n")
            previous_component = 1

            for component in block_components:
                if block_components.index(component) == 0:
                    continue
                else:
                    if component[0] != str(previous_component + 1):
                        raise ValueError(f"Block:\n\n{block}\n\nis not valid markdown")
                    previous_component =+ 1
            return "ordered_list"

        if block[-3:] not in markdown_indicators:
            raise ValueError(f"Block:\n{block}\nis not valid markdown")
        else:
            return markdown_indicators[block[:3]]

    if block[0] in markdown_indicators:
        if markdown_indicators[block[0]] == "unordered_list" or markdown_indicators[block[0]] == "quote":
            block_components = block.split("\n")
            for component in block_components:
                if component[0] != block[0]:
                    raise ValueError(f"Block:\n{block}\nis not valid markdown")
        return markdown_indicators[block[0]]

    return "paragraph"
