from textnode import *

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
