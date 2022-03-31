import sys 

from utils.executor import Executor
from utils.parser import Parser

p = Parser(str(sys.argv[1]))
paths, exprs, steps = p.run() 

result = Executor().evaluate_json_data(steps)
for res in result:
    print(res)
