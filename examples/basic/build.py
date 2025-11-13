from hashbuild import *
from os import path

src_base = path.dirname(__file__)
build_base = get_build_path()

info("a bunch of information")
warn("some warning")
error("fatal error oh nooo!!!")

obj = compile_file(f"{src_base}/test.c", f"{build_base}/basic.o")
link_objects(obj, f"{build_base}/basic.example")