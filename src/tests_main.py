from json import load, dumps
from utils.executor import Executor
from utils.parser import Parser

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()

p = Parser('/child::songs/child::song/child::title')
paths, exprs, steps = p.run() 

print(inferencer.get_schema())
print(inferencer.evaluate_steps(steps))
""" for key in schema:
    print(schema[key])
    print()

p = Parser('/child::songs/child::song')
_, _, steps = p.run() 
for step in steps:
    print(step) """

# print(data)
