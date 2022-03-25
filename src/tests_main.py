from json import load, dumps
from utils.executor import Executor

inferencer = Executor(open("json/basic.json"))
schema = inferencer.get_schema()
data = inferencer.get_data()

print(dumps(data, indent=2))
print(type(data["x"]) == dict)
print(type(data["x"]["a"]))

# print(dumps(schema, indent=2))
# print(dumps(schema["properties"], indent=2))
# a = a["x"]["a"]["b"]
# print(dumps(a, indent=2))
