import unittest

from textnode import *
from inline_markdown import *
class Tests(unittest.TestCase):
    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT.value)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE.value)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT.value),
            TextNode("code block", TextType.CODE.value),
            TextNode(" word", TextType.TEXT.value),
            ]
         )

    def test_split_node_bold(self):
        node = TextNode("This is text with a **BOLD** word", TextType.TEXT.value)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD.value)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT.value),
            TextNode("BOLD", TextType.BOLD.value),
            TextNode(" word", TextType.TEXT.value),
            ]
         )

    def test_split_node_italic(self):
        node = TextNode("This is text with an *ITALIC* word", TextType.TEXT.value)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC.value)

        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT.value),
            TextNode("ITALIC", TextType.ITALIC.value),
            TextNode(" word", TextType.TEXT.value),
            ]
         )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_links_expected(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev).", TextType.TEXT.value)
        self.assertEqual(split_nodes_link([node]), [
             TextNode("This is text with a link ", TextType.TEXT.value),
             TextNode("to boot dev", TextType.LINK.value, "https://www.boot.dev"),
             TextNode(".", TextType.TEXT.value),])

    def test_split_links_no_links(self):
        node = TextNode("This is text without any link", TextType.TEXT.value)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text without any link", TextType.TEXT.value)])

    def test_split_links_one_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT.value)
        self.assertEqual(split_nodes_link([node]), [
             TextNode("This is text with a link ", TextType.TEXT.value),
             TextNode("to boot dev", TextType.LINK.value, "https://www.boot.dev"),
             ])

    def test_split_image_expected(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev/image.png) and ![to youtube](https://www.youtube.com/@bootdotdev/another_image.png)", TextType.TEXT.value)
        self.assertEqual(split_nodes_image([node]), [
             TextNode("This is text with a link ", TextType.TEXT.value),
             TextNode("to boot dev", TextType.IMAGE.value, "https://www.boot.dev/image.png"),
             TextNode(" and ", TextType.TEXT.value),
             TextNode("to youtube", TextType.IMAGE.value, "https://www.youtube.com/@bootdotdev/another_image.png")
             ])

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        text_nodes = text_to_text_nodes(text)

        expected_output = [TextNode("This is ", TextType.TEXT.value, None), TextNode("text", TextType.BOLD.value, None), TextNode(" with an ", TextType.TEXT.value, None), TextNode("italic", TextType.ITALIC.value, None), TextNode(" word and a ", TextType.TEXT.value, None), TextNode("code block", TextType.CODE.value, None), TextNode(" and an ", TextType.TEXT.value, None), TextNode("obi wan image", TextType.IMAGE.value, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT.value, None), TextNode("link", TextType.LINK.value, "https://boot.dev")]
        self.assertEqual(text_nodes, expected_output)

if __name__ == "__main__":
    unittest.main()