import unittest

from inline_markdown import *

class Tests(unittest.TestCase):
    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
         )

    def test_split_node_bold(self):
        node = TextNode("This is text with a **BOLD** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
         )

    def test_split_node_italic(self):
        node = TextNode("This is text with an *ITALIC* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("ITALIC", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
         )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_links_expected(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev).", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(".", TextType.TEXT),])

    def test_split_links_no_links(self):
        node = TextNode("This is text without any link", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text without any link", TextType.TEXT)])

    def test_split_links_one_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             ])

    def test_split_image_expected(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev/image.png) and ![to youtube](https://www.youtube.com/@bootdotdev/another_image.png)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/image.png"),
             TextNode(" and ", TextType.TEXT),
             TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev/another_image.png")
             ])

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        text_nodes = text_to_text_nodes(text)

        expected_output = [TextNode("This is ", TextType.TEXT, None), TextNode("text", TextType.BOLD, None), TextNode(" with an ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" word and a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" and an ", TextType.TEXT, None), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT, None), TextNode("link", TextType.LINK, "https://boot.dev")]
        self.assertEqual(text_nodes, expected_output)

if __name__ == "__main__":
    unittest.main()