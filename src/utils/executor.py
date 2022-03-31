from pyjsonq import JsonQ
from genson import SchemaBuilder
from pymongo import MongoClient

from helpers.path import get_full_path, split_path
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
        schema_fields = set()

        def append_fields(sub_schema, path=""):
            if "properties" not in sub_schema:
                for attr in sub_schema:
                    if attr == "items":
                        append_fields(sub_schema[attr], path)
                        schema_fields.add(path)
                        return 
                    elif attr != "type":
                        schema_fields.add(get_full_path(path, attr))
                schema_fields.add(path)
            else:
                sub_schema = sub_schema["properties"]
                for attr in sub_schema:
                    if attr != "type":
                        append_fields(sub_schema[attr], get_full_path(path, attr))

                if path != "":
                    schema_fields.add(path)      

        append_fields(schema)
        return sorted(schema_fields)

    def evaluate_steps(self, steps):
        schema = self.get_schema()
        curr_levels = []

        for step in steps:
            if step.__class__.__name__ == "Path":
                axes, attr = step.get_parts()
                
                if axes == Axes.CHILD.value: 
                    if len(curr_levels) == 0: # If at root.
                        level = get_full_path("", attr)
                        
                        if level in schema: 
                            curr_levels.append(level)
                        else: 
                            print("Error in processing: ", level)
                            return 
                    else: 
                        level = get_full_path(level, attr)
                        curr_levels = list(filter(lambda a: a.endswith(level), schema))
                elif axes == Axes.DESCENDANT.value: 
                    if len(curr_levels) == 0: # If at root.
                        curr_levels = list(filter(lambda a: a.endswith(attr), schema))
                    else:
                        temp_levels = []
                    
                        for curr_level in curr_levels:
                            temp_levels = temp_levels + \
                                list(filter(lambda a: a.startswith(curr_level) and a.endswith(attr), schema))
                        
                        curr_levels = temp_levels

        return curr_levels

    def evaluate_json_data(self, steps, data=None): 
        if data is None: 
            data = self.get_json_data_all()

        paths = self.evaluate_steps(steps)
        if paths is None or len(paths) == 0:
            return []

        results = []
        
        for path in paths:
            temp_results = data
            for step in split_path(path):
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
