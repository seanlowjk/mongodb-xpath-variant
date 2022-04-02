from utils.executor import Executor
from utils.parser import Parser
from sys import exit 

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()

p = Parser('/songs/title')
paths, exprs, steps = p.run() 

print(inferencer.get_schema_tree())
"""
result = inferencer.evaluate_steps(steps)
for res in result:
    print(res)
"""

