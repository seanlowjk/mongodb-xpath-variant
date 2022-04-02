from utils.executor import Executor
from utils.parser import Parser

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()

p = Parser('/title')
paths, exprs, steps = p.run() 

schema = inferencer.get_schema() 

result = inferencer.evaluate_json_data(steps)
for res in result:
    print(res)
