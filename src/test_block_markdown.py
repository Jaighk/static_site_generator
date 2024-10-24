import unittest
from markdown_blocks import *

class Tests(unittest.TestCase):
    def test_example_expected(self):
        markdown_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected_result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(markdown_to_block(markdown_text), expected_result)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph block"
        self.assertEqual(block_to_block_type(block), MdBlockType.PARAGRAPH.value)

    def test_block_to_block_type_heading(self):
        block = "#This is a heading block"
        self.assertEqual(block_to_block_type(block), MdBlockType.HEADING.value)

    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        self.assertEqual(block_to_block_type(block), MdBlockType.CODE.value)

    def test_block_to_block_type_code_missing_close(self):
        block = "```This is a code block"
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_block_to_block_type_code_missing_open(self):
        block = "This is a code block```"
        self.assertEqual(block_to_block_type(block), MdBlockType.PARAGRAPH.value)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote block"
        self.assertEqual(block_to_block_type(block), MdBlockType.QUOTE.value)

    def test_block_to_block_type_quote_two_lines(self):
        block = ">This is a quote block\n>and this is the second line."
        self.assertEqual(block_to_block_type(block), MdBlockType.QUOTE.value)

    def test_block_to_block_type_quote_multiple_lines(self):
        block = ">This is a quote block\n>and this is the second line.\n>And a third for good measure"
        self.assertEqual(block_to_block_type(block), MdBlockType.QUOTE.value)

    def test_block_to_block_type_quote_multiple_lines_invalid(self):
        block = ">This is a quote block\nand this is the second line."
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_block_to_block_type_unordered_list(self):
        block = "*This is a unordered_list block"
        self.assertEqual(block_to_block_type(block), MdBlockType.ULIST.value)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a ordered_list block"
        self.assertEqual(block_to_block_type(block), MdBlockType.OLIST.value)

    def test_block_to_block_type_ordered_list_multiple_items(self):
        block = "1. This is a ordered_list block\n2. This is the second item"
        self.assertEqual(block_to_block_type(block), MdBlockType.OLIST.value)
        
    def test_block_to_block_type_ordered_list_multiple_items_broken(self):
        block = "1. This is a ordered_list block\nThis is the second item"
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_block_to_block_type_ordered_list_multiple_items_out_of_order(self):
        block = "1. This is a ordered_list block\n3. This is the second item"
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_markdown_to_htmlnode(self):
        self.maxDiff = None
        markdown = """# This is a heading.

This is a paragraph.

```
This is a code block
```

> This is a quote block
> this is another line.

* This is a UL
* This is the second list item

1. this is an ordered lists
2. this is the second item

[this is a link](https://youtube.com)

![this is an image](image.png)

"""
        expected_output = 'HTMLNode(div, None, [HTMLNode(h1, This is a heading, None, None), HTMLNode(p, This is a paragraph, None, None), HTMLNode(pre, None, HTMLNode(code, This is a code block, None, None), None), HTMLNode(blockquote, None, [HTMLNode(li, This is a quote block, None, None), HTMLNode(li, this is another line, None, None)], None), HTMLNode(ul, None, [HTMLNode(li, This is a UL, None, None), HTMLNode(li, This is the second list item, None, None)], None), HTMLNode(ol, None, [HTMLNode(li, this is an ordered lists, None, None), HTMLNode(li, 2. this is the second item, None, None)], None), HTMLNode(a, this is a link, None, https://youtube.com), HTMLNode(image, this is an image, None, image.png)], None)'
        self.assertEqual(str(markdown_to_htmlnode(markdown)), expected_output)

if __name__ == "__main__": 
    unittest.main()
