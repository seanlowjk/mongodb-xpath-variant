from utils.executor import Executor
from utils.parser import Parser

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()

p = Parser('/child::songs/descendant::title/parent::song/parent::songs')
paths, exprs, steps = p.run() 
result = inferencer.evaluate_json_data(steps)
for res in result:
    print(res)
