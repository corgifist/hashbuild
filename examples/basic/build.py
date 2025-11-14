from hashbuild import *
from os import path

src_base = path.dirname(__file__)
build_base = get_build_path()

obj = compile_file(f"{src_base}/test.c")
link_objects(obj, f"{build_base}/basic.example")