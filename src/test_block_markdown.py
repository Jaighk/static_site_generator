import unittest
from block_markdown import *

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
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_heading(self):
        block = "#This is a heading block"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type_code_missing_close(self):
        block = "```This is a code block"
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_block_to_block_type_code_missing_open(self):
        block = "This is a code block```"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_quote(self):
        block = ">This is a quote block"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_quote_two_lines(self):
        block = ">This is a quote block\n>and this is the second line."
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_quote_multiple_lines(self):
        block = ">This is a quote block\n>and this is the second line.\n>And a third for good measure"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_quote_multiple_lines_invadli(self):
        block = ">This is a quote block\nand this is the second line."
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_block_to_block_type_unordered_list(self):
        block = "*This is a unordered_list block"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a ordered_list block"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type_ordered_list_multiple_items(self):
        block = "1. This is a ordered_list block\n2. This is the second item"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        
    def test_block_to_block_type_ordered_list_multiple_items_broken(self):
        block = "1. This is a ordered_list block\nThis is the second item"
        self.assertRaises(ValueError, block_to_block_type, block)

    def test_block_to_block_type_ordered_list_multiple_items_out_of_order(self):
        block = "1. This is a ordered_list block\n3. This is the second item"
        self.assertRaises(ValueError, block_to_block_type, block)

if __name__ == "__main__": 
    unittest.main()
