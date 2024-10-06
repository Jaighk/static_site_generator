class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_string = ""
        if self.props == None:
            return ""
        for key in self.props:
            html_string += f' {key}="{self.props[key]}"'
        return html_string
    
    def __repr__(self):
        return f'''
        HTMLNode:
            \ttag: {self.tag}
            \tvalue: {self.value}
            \tchildren: {self.children}
            \tprops: {self.props}
        '''

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None: 
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(\"{self.tag}\", \"{self.value}\", \"{self.props}\")"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ValueError: tag not specified")
        if self.children == None:
            raise ValueError("ValueError: ParentNode has no children")

        child_html = ""

        for child in self.children:
            child_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
