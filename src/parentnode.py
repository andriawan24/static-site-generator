from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent node must have a tag")
        
        child_html = ""
        for child in self.children:
            if child.value == None:
                raise ValueError("All child must have value")
            
            child_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
        


