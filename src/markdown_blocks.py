
def markdown_to_block(markdown: str) -> list:
    blocks = []

    sections = markdown.split("\n\n")
    for section in sections:
        if section != "":
            blocks.append(section.strip())

    return blocks

def block_to_block_type(block: str) -> str:
    markdown_indicators = {
        "#": "heading",
        "```": "code",
        ">": "quote",
        "*": "unordered_list",
        "1. ": "ordered_list"}

    if block[:3] in markdown_indicators:
        if markdown_indicators[block[:3]] == "ordered_list":
            block_components = block.split("\n")
            previous_component = 1

            for component in block_components:
                if block_components.index(component) == 0:
                    continue
                else:
                    if component[0] != str(previous_component + 1):
                        raise ValueError(f"Block:\n\n{block}\n\nis not valid markdown")
                    previous_component =+ 1
            return "ordered_list"

        if block[-3:] not in markdown_indicators:
            raise ValueError(f"Block:\n{block}\nis not valid markdown")
        else:
            return markdown_indicators[block[:3]]

    if block[0] in markdown_indicators:
        if markdown_indicators[block[0]] == "unordered_list" or markdown_indicators[block[0]] == "quote":
            block_components = block.split("\n")
            for component in block_components:
                if component[0] != block[0]:
                    raise ValueError(f"Block:\n{block}\nis not valid markdown")
        return markdown_indicators[block[0]]

    return "paragraph"
