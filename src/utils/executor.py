from json import load, dumps
from os import pathsep
from numpy import identity
from pyjsonq import JsonQ
from genson import SchemaBuilder
from pymongo import MongoClient

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

    def get_random_document(self):
        results = self.collection.aggregate( \
            [{ "$sample": { "size": 1 } }] \
        )
        result = list(results)[0]
        del result['_id']
        return result

    def get_schema(self):
        self.builder.add_object(self.json_data)        
        schema = self.builder.to_schema()

        if not "properties" in schema:
            return []

        schema_fields = set()

        def get_field(path, key):
            if path == "":
                return key 

            return path + "." + key

        def append_fields(sub_schema, path=""):
            if "properties" not in sub_schema:
                for key in sub_schema:
                    if key == "items":
                        append_fields(sub_schema[key], path)
                        schema_fields.add(path)
                        return 
                    elif key != "type":
                        schema_fields.add(get_field(path, key))
                schema_fields.add(path)
            else:
                sub_schema = sub_schema["properties"]
                for key in sub_schema:
                    if key != "type":
                        append_fields(sub_schema[key], get_field(path, key))

                if path != "":
                    schema_fields.add(path)      

        append_fields(schema)
        return sorted(schema_fields)

    def evaluate_steps(self, steps):
        def get_field(path, key):
            if path == "":
                return key 

            return path + "." + key

        schema = self.get_schema()
        curr_levels = []

        for step in steps:
            if step.__class__.__name__ == "Path":
                axes, attr = step.get_parts()
                
                if axes == Axes.CHILD.value: 
                    if len(curr_levels) == 0:
                        level = get_field("", attr)
                        
                        if level in schema: 
                            curr_levels.append(level)
                        else: 
                            print("???")
                            return 
                    else: 
                        level = get_field(level, attr)
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

                       
    """def evaluate_data(self, levels, exprs, steps):
        expr_iter = 0
        self.curr_path = ''
        for level in levels:
            if expr_iter >= len(exprs):
                self.get_cur_res(level)
            else: 
                new_expr = exprs.at(expr_iter)
                if path == self.curr_path:
                    self.get_cur_res(level, new_expr)
                    expr_iter += 1
                else: 
                    self.get_cur_res(level)

        return self.curr_path.get()

    def get_cur_res(level, expr=None):
        level_arr = level.split('::')
        axis, identity = level_arr
        is_child = True # (right now) assume all are CHILD axis
        # if level_arr[0] == constants.Axes.CHILD:
        #     is_child = True

        if is_child:
            if expr is None:
                self.curr_path = self.qe.at(identity)
            else:
                if expr.is_unary_expr():
                    path, op, value, value_type = expr.to_parts()
                else:
                    path, op, value = expr.to_parts()
                path_axis, path_identity = path.get_levels()

                self.curr_path = self.qe.at(identity).where(path_identity, op, value)"""

    def has_path(self, path):
        return True 
