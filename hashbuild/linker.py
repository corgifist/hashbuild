from subprocess import Popen
from os import environ
from sys import stdout, stderr, stdin

from .compiler import ObjectFile

def get_linker_binary():
    if 'LD' in environ:
        return environ['LD']
    return 'cc'

def get_object_path(object: ObjectFile | str) -> str:
    if type(object) is str:
        return object
    return object.path

"""
you can use LD environment variable to change
the default linker (cc) to the one you'd like to use
"""
def link_objects(objects: list[ObjectFile | str] | ObjectFile | str, output: str) -> None:
    if type(objects) is not list:
        objects = [objects]
    command = []
    command.append(get_linker_binary())
    command.append("-o")
    command.append(output)
    for object in objects:
        command.append(get_object_path(object))
    
    process = Popen(command, stdout=stdout, stderr=stderr, stdin=stdin)
    process.wait()
