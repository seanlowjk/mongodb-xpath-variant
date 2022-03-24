from utils.parser import Parser

p = Parser('/child::bookstore[child::owner = "Sean Low"]/child::hero[child::age<=18]')
p.run() 
