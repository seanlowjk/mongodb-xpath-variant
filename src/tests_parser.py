from utils.parser import Parser

"""
p = Parser('/child::x/child::a[child::d = 0]/child::e[child::f != 0]')
levels, expressions, steps = p.run() 
for level in levels: print(level)
for expr in expressions: print(expr)
print()
"""

p = Parser('/child::songs[descendant::title="123"]')
levels, expressions, steps = p.run() 
for step in steps: print(step)
print()

"""
p = Parser('/ancestor-or-self::a')
levels, expressions, steps = p.run() 
for level in levels: print(level)
for expr in expressions: print(expr)
print()
"""

"""
p = Parser('/descendant-or-self::a')
levels, expressions, steps = p.run() 
for level in levels: print(level)
for expr in expressions: print(expr)
"""
