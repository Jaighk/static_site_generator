import unittest

from textnode import TextNode

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

    def url_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)

    def url_uneq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.google.com")
        self.assertNotEqual(node, node2)

    def url_uneq_none(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()