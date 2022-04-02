class SchemaNode: 
    def __init__(self, attr="Root", parent=None, children=dict()): 
        self.parent = parent 
        self.children = children 
        self.attr = attr

    def add_child(self, attr):
        self.children[attr] = SchemaNode(attr, self, dict())

    def add_path(self, path=[]):
        if len(path) == 0:
            return 

        curr_path = path[0]
        if not curr_path in  self.children:
            self.add_child(curr_path)

        path.pop(0)
        self.children[curr_path].add_path(path)

    def get_all_children(self):
        return self.children.values()

    def get_children(self, attr): 
        for child_attr in self.children: 
            if child_attr == attr:
                return [self.children[child_attr]]

        return []

    def get_descendant(self, attr): 
        descendants = self.get_children(attr)

        for child_attr in self.children: 
            child_node = self.children[child_attr]
            descendants = descendants + self.get_descendant(child_node, attr)

        return descendants

    def to_string(self, tabs=0):
        def get_string_repr():
            parent_key = "None" 
            if not self.parent is None: 
                parent_key = self.parent.attr 

            children_keys = list(map(lambda k: k.attr, list(self.children.values())))

            return "{} <- {} -> {}".format(parent_key, self.attr, children_keys)

        string_repr = ""
        for _ in range(0, tabs):
            string_repr = string_repr + "\t"

        return (string_repr + get_string_repr())

    def get_all_to_string(self, strings_list=[], tabs=0):
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
        return "\n".join(self.root.get_all_to_string())
