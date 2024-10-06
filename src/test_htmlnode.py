import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode(tag="a", value="A Link", props={"href": "https://www.google.com", "target": "_blank",})
        self.assertIsInstance(node, HTMLNode)
    
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="A Link", props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_not_none(self):
        node = HTMLNode(tag="a", value="A Link", children="child", props={"href": "https://www.google.com", "target": "_blank",})
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.children)
        self.assertIsNotNone(node.props)

    def test_is_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

class TestLeafNode(unittest.TestCase):
    def test_LeafNode_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_LeafNode_print(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertIsInstance(node, LeafNode)

class TestParentNode(unittest.TestCase):
    def test_ParentNode_example(self):
        node = ParentNode("p",
                [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag(self):
        node = ParentNode(None, LeafNode("p","This is a p tag"))
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

if __name__ == "__main__": 
    unittest.main()
