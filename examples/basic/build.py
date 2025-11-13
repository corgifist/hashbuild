from hashbuild import *
from os import path

base = path.dirname(__file__)
obj = compile_file(f"{base}/test.c", f"{base}/basic.o")
link_objects(obj, f"{base}/basic.example")