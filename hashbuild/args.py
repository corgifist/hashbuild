from .utils import *

from argparse import ArgumentParser
from pathlib import Path
from os import path, mkdir

parser = ArgumentParser()
parser.add_argument('-b', '--build', type=Path, required=False, default='.', \
    help='a path to the directory where compiled binaries will be stored'
)
parser.add_argument(
    '-c', '--cache', type=Path, required=False, default='.', \
    help='a path to the directory where HashBuild will create .hashbuild folder'
)

args = parser.parse_args()

def get_build_path():
    return args.build

def get_cache_path():
    return args.cache

build = get_build_path()
cache = get_cache_path()

if not path.exists(f"{cache}/.hashbuild/"):
    info(f"{cache}/.hashbuild/ does not exist, creating...")
    mkdir(f"{cache}/.hashbuild")

if not path.exists(f"{build}/"):
    info(f"./{build}/ does not exist, creating...")
    mkdir(f"./{build}")