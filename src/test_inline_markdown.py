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

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        
    def test_extract_images_unmatched_alt_text(self):
        with self.assertRaises(ValueError):
            text = "This is text with a ![rick roll] and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            extract_markdown_images(text)

    def test_extract_images_unmatched_url_text(self):
        with self.assertRaises(ValueError):
            text = "This is text with a (https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            extract_markdown_images(text)

    def text_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_mardown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_links_unmatched_url(self):
        with self.assertRaises(ValueError):
            text = "This is text with a link (https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            extract_markdown_images(text)

    def test_extract_links_unmatched_link_text(self):
        with self.assertRaises(ValueError):
            text = "This is text with a link [to boot dev] and [to youtube](https://www.youtube.com/@bootdotdev)"
            extract_markdown_images(text)

if __name__ == "__main__":
    unittest.main()
