import unittest

from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
    
    def test_text_type_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_text_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_url_uneq_none(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        # text, type, url=None

        text_node_text = TextNode("this is text", TextType.TEXT)
        text_node_bold = TextNode("this is bold", TextType.BOLD)
        text_node_italic = TextNode("this is italic", TextType.ITALIC)
        text_node_code = TextNode("this is code", TextType.CODE)
        text_node_link = TextNode("this is link", TextType.LINK, "https://www.google.com")
        text_node_image = TextNode("this is image", TextType.IMAGE, "https://www.google.com/images")

        self.assertIsInstance(text_node_to_html_node(text_node_text), LeafNode)
        self.assertIsInstance(text_node_to_html_node(text_node_bold), LeafNode)
        self.assertIsInstance(text_node_to_html_node(text_node_italic), LeafNode)
        self.assertIsInstance(text_node_to_html_node(text_node_code), LeafNode)
        self.assertIsInstance(text_node_to_html_node(text_node_link), LeafNode)
        self.assertIsInstance(text_node_to_html_node(text_node_image), LeafNode)


if __name__ == "__main__":
    unittest.main()
