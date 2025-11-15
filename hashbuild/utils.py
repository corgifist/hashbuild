from colorama import Fore
from os import cpu_count, path
from hashlib import sha1
from pathlib import Path

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

"""
notice: extensions must start with dot! (e.g '.py', '.cpp' etc.)
        extensions argument is either string of extensions separated by comma
        e.g. ".py,.cpp,.c"
        or a list of strings
        e.g. ['.py', '.cpp', '.c']
"""
def glob_files(path: Path | str, extensions: str | list[str] = None, recursive: bool = True) -> list[Path]:
    if type(path) is str:
        path = Path(path)
    if extensions is not None and type(extensions) is str:
        extensions = extensions.split(',')
    result = []
    for file in path.iterdir():
        if file.is_dir():
            if recursive:
                result += glob_files(file, extensions=extensions, recursive=recursive)
            continue
        if extensions is not None:
            ext = file.suffix
            skip = True
            for filter in extensions:
                if ext == filter:
                    skip = False 
                    break
            if skip:
                continue
        result.append(file)
    return result