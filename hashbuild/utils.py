from colorama import Fore
from os import cpu_count, path
from hashlib import sha1

concurrency = cpu_count()

def info(*args):
    print(Fore.CYAN, "info: ", Fore.RESET, *args, sep='')

def warn(*args):
    print(Fore.YELLOW, "warning: ", Fore.RESET, *args, sep='')

def error(*args):
    print(Fore.RED, "error: ", Fore.RESET, *args, sep='')

def hash_string(str: str) -> str:
    return sha1(str.encode('utf-8')).hexdigest()[0:10]

def get_modification_date(path: str):
    return path.getmtime(path)

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    with open(path, 'w+') as f:
        f.write(content)