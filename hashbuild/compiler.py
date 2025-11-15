# crucial for spawning compiler processes
from subprocess import Popen
from os import environ, path
from sys import stdout, stdin, stderr
from .args import get_cache_path
from .utils import *

class ObjectFile:
    def __init__(self, source, path, fresh=True, cxx=False):
        self.source = source
        self.path = path
        self.fresh = fresh
        self.cxx = cxx

def get_compiler_binary() -> str:
    if 'CC' in environ:
        return environ['CC']
    return "cc"

def get_object_path_stem(input: str) -> str:
    return f'{get_cache_path()}/.hashbuild/{hash_string(input)}'

"""
By default compile_file uses `cc` to compile files, but
if you'd like to change this behavior, set CC environment variable
to your desired compiler e.g.:
```
~ CC=gcc
~ python build.py (HashBuild will call gcc directly)
```
"""
def compile_file(input: Path | str, output: str = None, flags: list[str] =[], cxx: bool = False, throw: bool = True) -> ObjectFile:
    if type(input) is not str:
        input = str(input)
    if not path.exists(input):
        if throw:
            raise RuntimeError(f"file '{input}' does not exist")
        return None
    source_code_hash = hash_string(read_file(input) + f"\n{flags}")
    object_stem = None
    if output is None:
        object_stem = get_object_path_stem(input)
        output = object_stem + '.o'
    else:
        object_stem = str(path.splitext(output)[0])
    result = ObjectFile(
        input,
        output, 
        cxx
    )
    # no need to recompile file
    if path.exists(object_stem + '.compiler_hash') and read_file(object_stem + '.compiler_hash') == source_code_hash:
        result.fresh = False
        return result
    command = []
    command.append(get_compiler_binary())
    command.append("-c")
    command.append(input)
    command.append("-o")
    command.append(output)
    for flag in flags:
        command.append(flag)

    handle = Popen(command, stdout=stdout, stdin=stdin, stderr=stderr)
    status = handle.wait()
    if status != 0:
        raise RuntimeError(f"failed to compile {input}")
    write_file(object_stem + '.compiler_hash', source_code_hash)
    result.fresh = True
    return result