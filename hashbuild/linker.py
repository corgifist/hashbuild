from subprocess import Popen
from os import environ
from sys import stdout, stderr, stdin

from .compiler import ObjectFile
from .utils import *
from .args import *

def get_linker_binary():
    if 'LD' in environ:
        return environ['LD']
    return 'cc'

def get_object_path(object: ObjectFile | str) -> str:
    if type(object) is str:
        return object
    return object.path

def is_object_fresh(object: ObjectFile | str) -> bool:
    if type(object) is str:
        return True
    return object.fresh

"""
you can use LD environment variable to change
the default linker (cc) to the one you'd like to use
"""
def link_objects(objects: list[ObjectFile | str] | ObjectFile | str, output: str, flags: list[str] = []) -> None:
    if type(objects) is not list:
        objects = [objects]
    cache_path = f"{get_cache_path()}/.hashbuild"
    state_hash = hash_string(f"{list(map(lambda object: get_object_path(object), objects))}{flags}")
    output_hash = hash_string(output)
    needs_recompilation = False
    if not path.exists(f"{cache_path}/{output_hash}.linker_hash"):
        needs_recompilation = True
    elif read_file(f"{cache_path}/{output_hash}.linker_hash") != state_hash:
        needs_recompilation = True
    for object in objects:
        if is_object_fresh(object):
            needs_recompilation = True
            break
    if not needs_recompilation:
        return
    command = []
    command.append(get_linker_binary())
    command.append("-o")
    command.append(output)
    for object in objects:
        command.append(get_object_path(object))
    for flag in flags:
        command.append(flag)
    
    process = Popen(command, stdout=stdout, stderr=stderr, stdin=stdin)
    status = process.wait()
    if status == 0:
        write_file(f"{cache_path}/{output_hash}.linker_hash", state_hash)
