from utils.parser import Parser

p = Parser('/child::x/child::a[child::d = 0]/child::e[child::f != 0]')
levels, expressions, steps = p.run() 
for level in levels: print(level)
for expr in expressions: print(expr)

