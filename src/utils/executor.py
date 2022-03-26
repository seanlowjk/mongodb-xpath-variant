from json import load
from pyjsonq import JsonQ
from genson import SchemaBuilder

import constants

class Executor:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.qe = JsonQ(self.json_file_path)
        self.builder = SchemaBuilder()

    def get_json_data(self):
        self.json_data = load(open(self.json_file_path))

    '''
    Retrieves schema in JSON format in self.keys
    '''
    def get_schema(self):
        self.builder.add_object(self.json_data)        
        schema = self.builder.to_schema()
        qe = JsonQ(data=schema)
        self.keys = qe.at('properties')
        # print(self.keys.get())

        # next_level = self.keys.at('x').at('properties').at('a')
        # next level down should either be items or properties (check their keys first)
        # print(next_level.get().keys())
        # print(self.keys.get())

    def evaluate_data(self, parsed_info):
        levels, exprs = parsed_info
        expr_iter = 0
        self.curr_path = ''
        for level in levels:
            if expr_iter >= len(exprs):
                self.curr_path = self.get_cur_res(level)
            else: 
                new_expr = exprs.at(expr_iter)
                # check what kind of expr it is (unary or binary), need different API
                path, op, value, value_type = new_expr.to_parts()
                if path == self.curr_path:
                    self.curr_path = self.get_cur_res(level, new_expr)
                    expr_iter += 1
                else: 
                    self.curr_path = self.get_cur_res(level)

        return self.curr_path.get()

    def get_cur_res(level, expr=None):
        level_arr = level.split('::')
        is_child = False
        if level_arr[0] == constants.Axes.CHILD:
            is_child = True

        if is_child:
            if expr is None:
                self.curr_path = self.qe.at(level)
            else:
                # check type of expr
                path, op, value, value_type = expr.to_parts()
                self.curr_path = self.qe.at(level).where(op, value_type, value) # confirm what the prev method returns

    def has_path(self, path):
        return True 
