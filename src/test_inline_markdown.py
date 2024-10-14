import unittest

from inline_markdown import *

class Tests(unittest.TestCase):
    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
            ]
         )

    def test_split_node_bold(self):
        node = TextNode("This is text with a **BOLD** word", text_type_text)
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

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_links_expected(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
        self.assertEqual(split_nodes_link([node]), [
             TextNode("This is text with a link ", text_type_text),
             TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
             TextNode(" and ", text_type_text),
             TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev")
             ])

    def test_split_links_no_links(self):
        node = TextNode("This is text without any link", text_type_text)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text without any link", text_type_text)])

    def test_split_links_one_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", text_type_text)
        self.assertEqual(split_nodes_link([node]), [
             TextNode("This is text with a link ", text_type_text),
             TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
             ])

    def test_split_image_expected(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev/image.png) and ![to youtube](https://www.youtube.com/@bootdotdev/another_image.png)", text_type_text)
        self.assertEqual(split_nodes_image([node]), [
             TextNode("This is text with a link ", text_type_text),
             TextNode("to boot dev", text_type_image, "https://www.boot.dev/image.png"),
             TextNode(" and ", text_type_text),
             TextNode("to youtube", text_type_image, "https://www.youtube.com/@bootdotdev/another_image.png")
             ])

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        text_nodes = text_to_text_nodes(text)

        expected_output = [TextNode("This is ", "text", None), TextNode("text", "bold", None), TextNode(" with an ", "text", None), TextNode("italic", "italic", None), TextNode(" word and a ", "text", None), TextNode("code block", "code", None), TextNode(" and an ", "text", None), TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", "text", None), TextNode("link", "link", "https://boot.dev")]
        self.assertEqual(text_nodes, expected_output)

if __name__ == "__main__":
    unittest.main()
