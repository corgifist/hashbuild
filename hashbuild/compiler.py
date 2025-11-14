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

def get_compiler_binary():
    if 'CC' in environ:
        return environ['CC']
    return "cc"

"""
By default compile_file uses `cc` to compile files, but
if you'd like to change this behavior, set CC environment variable
to your desired compiler e.g.:
```
~ CC=gcc
~ python build.py (HashBuild will call gcc directly)
```
"""
def compile_file(input: str, output: str = None, flags: list[str] =[]) -> ObjectFile:
    if not path.exists(input):
        raise RuntimeError(f"file '{input}' does not exist")
    source_code_hash = hash_string(read_file(input) + f"\n{flags}")
    input_hash = hash_string(input)
    cache_path = f"{get_cache_path()}/.hashbuild"
    base_path = f"{cache_path}/{input_hash}"
    if output is None:
        output = base_path + '.o'
    result = ObjectFile(
        input,
        output, 
        False
    )
    # no need to recompile file
    if path.exists(base_path + '.compiler_hash') and read_file(base_path + '.compiler_hash') == source_code_hash:
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
    write_file(base_path + '.compiler_hash', source_code_hash)
    result.fresh = True
    return result