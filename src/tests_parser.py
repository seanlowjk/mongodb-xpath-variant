from utils.parser import Parser

p = Parser('/child::x/child::a[child::d = 0]/child::e[child::f != 0]')
p.run() 

