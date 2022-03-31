from json import load, dumps
from os import pathsep
from numpy import identity
from pyjsonq import JsonQ
from genson import SchemaBuilder
from pymongo import MongoClient

from helpers.path import get_full_path
from utils.constants import Axes

class Executor:
    def __init__(self, json_file_path, db="test", collection="library"):
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

        return curr_levels

    def evaluate_json_data(self, steps, data=None): 
        if data is None: 
            data = self.get_json_data_all()

        paths = self.evaluate_steps(steps)
        results = data

        def split_path(path):
            return path.split(".")
        
        for path in paths:
            for step in split_path(path):
                temp_data = []

                for temp in results:
                    if step in temp:
                        res = temp[step]
                        if type(res).__name__ == "list":
                            for res_elem in res: 
                                temp_data.append(res_elem)
                        else: 
                            temp_data.append(res)
                
                results = temp_data

        return results

    def has_path(self, path):
        return True 
