from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if delimiter == "":
            new_nodes.append(TextNode(old_node.text, text_type_text))
            continue

        text_sections = old_node.text.split(delimiter)

        if len(text_sections) % 2 == 0:
            raise ValueError("Invalid Markdown: missing closing markdown formatter")

        for i in range(len(text_sections)):
            if i % 2 != 0 :
                new_nodes.append(TextNode(text_sections[i], text_type))
            else:
                new_nodes.append(TextNode(text_sections[i], text_type_text))

    return new_nodes

def extract_markdown_images(text):
    image_properties = []

    alt_texts= re.findall(r"\[(.*?)\]", text)
    urls = re.findall(r"\((.*?)\)", text)
    
    if len(alt_texts) != len(urls):
        raise ValueError("Unmatched alt text or url")

    for image in alt_texts:
        image_index = alt_texts.index(image)
        image_properties.append((image, urls[image_index]))

    return image_properties

def extract_mardown_links(text):
    link_properties = []

    link_text = re.findall(r"\[(.*?)\]", text)
    urls = re.findall(r"\((.*?)\)", text)
    
    if len(link_text) != len(urls):
        raise ValueError("Unmatched link text or url")

    for link in link_text:
        link_index = link.index(link_text)
        link_properties.append((link, urls[link_index]))

    return link_properties
