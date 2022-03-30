from json import load, dumps
from numpy import identity
from pyjsonq import JsonQ
from genson import SchemaBuilder
from pymongo import MongoClient

class Executor:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.qe = JsonQ(self.json_file_path)
        self.builder = SchemaBuilder()
        self.db = MongoClient()["test"]

    def get_json_data(self):
        self.json_data = self.get_random_document()

    def get_random_document(self):
        results = self.db.library.aggregate( \
            [{ "$sample": { "size": 1 } }] \
        )
        result = list(results)[0]
        del result['_id']
        return result

    '''
    Retrieves schema in JSON format in self.keys
    '''
    def get_schema(self):
        self.builder.add_object(self.json_data)        
        schema = self.builder.to_schema()
        qe = JsonQ(data=schema)
        return schema
        # self.keys = qe.at('properties')
        # print(self.keys.get())

        # next_level = self.keys.at('x').at('properties').at('a')
        # next level down should either be items or properties (check their keys first)
        # print(next_level.get().keys())
        # print(self.keys.get())

    def evaluate_data(self, levels, exprs):
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
                path_axis, path_identity = path.split('::')

                self.curr_path = self.qe.at(identity).where(path_identity, op, value) 

    def has_path(self, path):
        return True 
