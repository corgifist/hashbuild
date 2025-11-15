from hashbuild import *
from os import path

src_base = path.relpath(path.dirname(__file__))
sum_library = library(
    f'{src_base}/dynamic_library.cpp', 
    'sum', 
    definitions={
        'EXPORTING_SYMBOLS': 1
    },
    cxx=True
)
divide_library = library(
    f'{src_base}/static_library.cpp',
    'divide',
    definitions={
        'EXPORTING_SYMBOLS': 1
    },
    type='static',
    cxx=True
)

executable(
    f'{src_base}/main.cpp',
    'arithmetic.example',
    cxx=True,
    libraries=[
        sum_library, divide_library
    ]
)
