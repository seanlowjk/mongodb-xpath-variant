from utils.executor import Executor
from utils.parser import Parser

inferencer = Executor("json/basic.json")
data = inferencer.get_json_data()

p = Parser('/child::songs[descendant::title="Separuh Jiwaku Pergi"]/descendant::title')
paths, exprs, steps = p.run() 

result = inferencer.evaluate_json_data(steps)
for res in result:
    print(res)

# title / songs.song.title
# res = list(inferencer.collection.find(\
#    { "$and": [{ "songs.song.title": {"$eq": "Separuh Jiwaku Pergi" }}]},\
# { "_id": 0, "title": 1 }))
# print(res)

# res = list(inferencer.collection.find(\
#    { "$and": [{ "songs.song.title": {"$eq": "Separuh Jiwaku Pergi" }}]},\
# { "_id": 0, "songs.song.title": 1 }))
# print(res[0])
