from input_stream import input_stream
from token_stream import token_stream
from parser import parse

code = input()
ast = parse(token_stream(input_stream(code)))