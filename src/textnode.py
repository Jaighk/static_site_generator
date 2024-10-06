from htmlnode import *

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def text_node_to_html_node(self):
        if self.text_type == "text":
            return LeafNode(None, self.text)
        if self.text_type == "bold":
            return LeafNode("b", self.text)
        if self.text_type == "italic":
            return LeafNode("i", self.text)
        if self.text_type == "code":
            return LeafNode("code", self.text)
        if self.text_type == "link":
            return LeafNode("a", self.text, props={"href": f"{self.url}"})
        if self.text_type == "image":
            return LeafNode("i", "", props={ "src": f"{self.url}", "alt": f"{self.text}"})
        raise ValueError(f"ValueError: text_type \"{self.text_type}\" not supported")
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

