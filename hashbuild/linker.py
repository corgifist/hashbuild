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
def link_objects(objects: list[ObjectFile | str] | ObjectFile | str, output: str, cxx: bool = False, libraries: list[str] = [], flags: list[str] = [], binary_type: str = 'executable') -> None:
    if type(objects) is not list:
        objects = [objects]
    cache_path = f"{get_cache_path()}/.hashbuild"
    state_hash = hash_string(f"{list(map(lambda object: get_object_path(object), objects))}{flags}{binary_type}")
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
    command.append(f'-L{get_build_path()}/')
    if binary_type == 'shared':
        command.append('-shared')
    elif binary_type == 'static':
        command.append('-static')
    command.append("-o")
    command.append(output)
    for object in objects:
        command.append(get_object_path(object))
    if cxx:
        command.append('-lstdc++')
    for flag in flags:
        command.append(flag)
    for library in libraries:
        command.append(library if '/' in library or '\\' in library else '-l{library}')
    # info(' '.join(command))
    process = Popen(command, stdout=stdout, stderr=stderr, stdin=stdin)
    status = process.wait()
    if status == 0:
        write_file(f"{cache_path}/{output_hash}.linker_hash", state_hash)
    else:
        error(f'failed to link {binary_type if binary_type == 'executable' else binary_type + ' library'} {output}')
        exit(1)
