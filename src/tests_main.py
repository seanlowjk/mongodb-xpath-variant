from json import load, dumps
from utils.executor import Executor

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()
schema = inferencer.get_schema()

# print(data)
