import unittest

from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)
    
    def test_text_type_uneq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "code")
        self.assertNotEqual(node, node2)

    def test_text_uneq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is also a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_uneq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_url_uneq_none(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        # text, type, url=None

        text_node_text = TextNode("this is text", "text")
        text_node_bold = TextNode("this is bold", "bold")
        text_node_italic = TextNode("this is italic", "italic")
        text_node_code = TextNode("this is code", "code")
        text_node_link = TextNode("this is link", "link", "https://www.google.com")
        text_node_image = TextNode("this is image", "image", "https://www.google.com/images")

        self.assertIsInstance(text_node_text.text_node_to_html_node(), LeafNode)
        self.assertIsInstance(text_node_bold.text_node_to_html_node(), LeafNode)
        self.assertIsInstance(text_node_italic.text_node_to_html_node(), LeafNode)
        self.assertIsInstance(text_node_code.text_node_to_html_node(), LeafNode)
        self.assertIsInstance(text_node_link.text_node_to_html_node(), LeafNode)
        self.assertIsInstance(text_node_image.text_node_to_html_node(), LeafNode)


if __name__ == "__main__":
    unittest.main()
