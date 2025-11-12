from hashbuild import *
from os import path

compile_file(f"{path.dirname(__file__)}/test.c", output="test.o")