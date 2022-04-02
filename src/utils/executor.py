from pyjsonq import JsonQ
from genson import SchemaBuilder
from pymongo import MongoClient

from helpers.path import get_full_path
from objects.schema import SchemaTree
from utils.constants import Axes

class Executor:
    def __init__(self, json_file_path="", db="test", collection="library"):
        self.json_file_path = json_file_path
        self.qe = JsonQ(self.json_file_path)
        self.builder = SchemaBuilder()

        self.collection = MongoClient()[db][collection]

    def get_json_data_all(self):
        return list(self.collection.find())

    def get_json_data(self):
        self.json_data = self.get_random_document()

    def get_random_document(self, has_id=False):
        results = self.collection.aggregate([{ "$sample": { "size": 1 } }])
        result = list(results)[0]

        if not has_id: 
            del result['_id']
        return result

    def get_schema(self):
        self.get_json_data()
        self.builder.add_object(self.json_data)        
        schema = self.builder.to_schema()
        if not "properties" in schema:
            return []
        schema_tree = SchemaTree()

        def add_key(key, schema_tree=schema_tree):
            if key is None:
                return 

            schema_tree.add_path(key)

        def append_fields(sub_schema, path=[]):
            if "properties" not in sub_schema:
                for attr in sub_schema:
                    if attr == "items":
                        append_fields(sub_schema[attr], path)
                        add_key(path)
                        return 
                    elif attr != "type":
                        add_key(get_full_path(path, attr))
                add_key(path)
            else:
                sub_schema = sub_schema["properties"]
                for attr in sub_schema:
                    if attr != "type":
                        append_fields(sub_schema[attr], get_full_path(path, attr))

                if path != "":
                    add_key(path)     

        append_fields(schema)
        return schema_tree

    def evaluate_steps(self, steps):
        def call_api(curr_nodes, node_method):
            output_nodes = []

            for node in curr_nodes: 
                func = getattr(node, node_method)
                output_nodes = output_nodes + func(attr)

            return output_nodes
        
        schema = self.get_schema()
        curr_nodes = [schema.root]

        for step in steps:
            if step.__class__.__name__ == "Path":
                axes, attr = step.get_parts()
                
                if axes == Axes.CHILD.value: 
                    output_nodes = call_api(curr_nodes, "get_children")
                    if len(output_nodes) == 0:
                        return []

                    curr_nodes = output_nodes
                elif axes == Axes.DESCENDANT.value: 
                    output_nodes = call_api(curr_nodes, "get_descendants")
                    if len(output_nodes) == 0:
                        return []

                    curr_nodes = output_nodes
                elif axes == Axes.PARENT.value: 
                    output_nodes = call_api(curr_nodes, "get_parent")
                    if len(output_nodes) == 0:
                        return []

                    curr_nodes = output_nodes
                """
                elif axes == Axes.ANCESTOR.value:
                    if len(curr_level) == 0:
                        return 
                    else:
                        temp_levels = []
                        indexes = list()
                        for curr_level in curr_levels:
                            # crawl back
                            curr_index = schema.index(curr_level)
                            indexes.append(curr_index)
                            # find all index of this node
                            while (curr_index +1) < len(schema):
                                curr_index = schema.index(curr_level, curr_index +1)
                                indexes.append(curr_index)
                        
                        max_index = max(indexes)

                        for i in range(0, max_index+1):
                            if(schema[i].endswith(attr)):
                                temp_levels.append(schema[i])
                        
                        curr_levels = temp_levels
                """
                            
        return curr_nodes

    def evaluate_json_data(self, steps, data=None): 
        if data is None: 
            data = self.get_json_data_all()

        schemas = self.evaluate_steps(steps)
        if schemas is None or len(schemas) == 0:
            return []

        results = []

        for schema in schemas:
            temp_results = data

            for step in schema.to_path():
                temp_data = temp_results
                temp_next = []

                for temp in temp_data:
                    if step in temp:
                        res = temp[step]
                        if type(res).__name__ == "list":
                            for res_elem in res: 
                                temp_next.append(res_elem)
                        else: 
                            temp_next.append(res)
                
                temp_results = temp_next
            results = results + temp_results

        return results
