import unittest

from inline_markdown import *

class Test_example(unittest.TestCase):
    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
            ]
         )

    def test_split_node_text(self):
        node = TextNode("This is text with a text block", text_type_text)
        new_nodes = split_nodes_delimiter([node], "", text_type_text)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a text block", text_type_text)
            ]
         )

    def test_split_node_bold(self):
        node = TextNode("This is text with a **BOLD** word", text_type_bold)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("BOLD", text_type_bold),
            TextNode(" word", text_type_text),
            ]
         )

    def test_split_node_italic(self):
        node = TextNode("This is text with a *ITALIC* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("ITALIC", text_type_italic),
            TextNode(" word", text_type_text),
            ]
         )

if __name__ == "__main__":
    unittest.main()
