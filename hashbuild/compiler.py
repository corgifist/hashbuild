# crucial for spawning compiler processes
from subprocess import Popen
from os import environ
from sys import stdout, stdin, stderr

class ObjectFile:
    def __init__(self, path, cxx=False):
        self.path = path
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
def compile_file(input: str, output: str = None) -> ObjectFile:
    command = []
    command.append(get_compiler_binary())
    command.append("-c")
    command.append(input)
    command.append("-o")
    command.append(output)

    handle = Popen(command, stdout=stdout, stdin=stdin, stderr=stderr)
    handle.wait()
    return ObjectFile(
        output, 
        False
    )