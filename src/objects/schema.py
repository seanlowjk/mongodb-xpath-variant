class SchemaNode: 
    def __init__(self, attr=None, parent=None, children=dict()): 
        self.parent = parent 
        self.children = children 
        self.attr = attr

    def __str__(self):
        return "\n".join(self.get_all_to_string())

    def to_path(self):
        """
        Converts the node to a path for data retrieval. 
        """
        if self.attr is None: # Means at Root
            return []

        parent_node = self.parent

        path = [self.attr]
        while not parent_node is None and not parent_node.attr is None:
            path = [parent_node.attr] + path
            parent_node = parent_node.parent 

        return path 
        
    def add_child(self, attr):
        """
        Adds a child node to the current node. 
        """
        self.children[attr] = SchemaNode(attr, self, dict())

    def add_path(self, path=[]):
        """
        Adds a path to the current node. 
        """
        if len(path) == 0:
            return 

        curr_path = path[0]
        if not curr_path in  self.children:
            # Add a new child node if curr_path DOES NOT exist.
            self.add_child(curr_path)

        path.pop(0)
        self.children[curr_path].add_path(path)

    def get_children(self, attr): 
        """
        Gets the children of the current node. 
        Note that it is returned as a list. 
        """
        for child_attr in self.children: 
            if child_attr == attr:
                return [self.children[child_attr]]

        return []

    def get_descendants(self, attr): 
        """
        Gets all the descendants of the current node. 
        """
        descendants = self.get_children(attr)

        for child_attr in self.children: 
            child_node = self.children[child_attr]
            descendants = descendants + child_node.get_descendants(attr)
        
        return descendants

    def get_parent(self, attr):
        """
        Gets the parent of the current node. 
        Note that it is returned as a list. 
        """
        if not self.parent is None and self.parent.attr == attr:
            return [self.parent]

        return []

    def get_ancestors(self, attr):
        """
        Gets the get_ancestors of the current node. 
        """
        ancestors = self.get_parent(attr)
        parent_node = self.parent

        while not parent_node is None: 
            ancestors = ancestors + parent_node.get_parent(attr)
            parent_node = parent_node.parent

        return ancestors

    def to_string(self, tabs=0):
        """
        Gets its own strings representation as a string. 

        Pads the front with tabs depending on the nesting level of the node.
        """
        def get_string_repr():
            parent_key = "None" 
            if not self.parent is None: 
                parent_key = self.parent.attr 

            attr = "Root"
            if not self.attr is None: 
                attr = self.attr

            children_keys = list(map(lambda k: k.attr, list(self.children.values())))

            return "{} <- {} -> {}".format(parent_key, attr, children_keys)

        string_repr = ""
        for _ in range(0, tabs):
            string_repr = string_repr + "\t"

        return (string_repr + get_string_repr())

    def get_all_to_string(self, strings_list=[], tabs=0):
        """
        Get strings representation of itself and its 
        children in a list. 
        """
        strings_list = strings_list + [self.to_string(tabs)]
        for child in self.children.values():
            strings_list = child.get_all_to_string(strings_list, tabs + 1)

        return strings_list

class SchemaTree: 
    def __init__(self):
        self.root = SchemaNode()

    def add_path(self, path=[]):
        self.root.add_path(path)

    def __str__(self):
        return str(self.root)
