from utils.executor import Executor
from utils.parser import Parser

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()

p = Parser('/songs/title')
paths, exprs, steps = p.run() 

schema = inferencer.get_schema() 
print(schema)
"""
result = inferencer.evaluate_steps(steps)
for res in result:
    print(res)
"""

