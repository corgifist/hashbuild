from hashbuild import *
from os import path

executable(
    glob_files(path.dirname(__file__), '.c'),
    'basic'
)