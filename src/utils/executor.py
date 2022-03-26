from json import load
from pydantic import Json
from pyjsonq import JsonQ

class Executor:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.qe = JsonQ(self.json_file_path)

    def get_json_data(self):
        json_data = load(open(self.json_file_path))
        print(json_data.keys())
    

    # def evaluate_data(self, parsed_info):
    #     levels, exprs = parsed_info # ['child::x', 'child::a', 'child::e'] - paths.get_levels(), [(2:expr), (3:expr)]
    #     i = 1 
    #     for level in levels:
    #         if i in exprs:
    #             res = self.get_cur_res(level, exprs.get(i))
    #         else:
    #             res = self.get_cur_res(level)
    #         i += 1

    #     res = self.qe.at('x').at('a').where('d', '=', "3").get()
    #     return res

    # def get_cur_res(level, expr=None):
    #     # attr = get_attribute(level)
    #     # expr:
    #     # - remove child::
    #     # - split into 3 part (key, operator, value)
    #     if expr is None:
    #         res = self.qe.at(level).get()
    #     else:
    #         res = self.qe.at(level).where(expr).get()
    #     return res

    def has_path(self, path):
        return True 
