from utils.parser import Parser

p = Parser('/child::a[child::b < "j k" or child::c > 3 and child::d = 0]/child::e[child::f != 0]')
p.run() 
