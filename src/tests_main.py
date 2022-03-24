from json import load, dumps

a = load(open("json/basic.json"))
a = a["schools"]
print(dumps(a, indent=2))
