from utils.parser import Parser

p = Parser('/child::bookstore[child::owner = "Sean Low" and child::owner = "Seans Lows"]/child::owner[child::age<=18]')
p.run() 
