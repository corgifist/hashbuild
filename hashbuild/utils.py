from colorama import Fore

def info(*args):
    print(Fore.CYAN, "info: ", Fore.RESET, *args, sep='')

def warn(*args):
    print(Fore.YELLOW, "warning: ", Fore.RESET, *args, sep='')

def error(*args):
    print(Fore.RED, "error: ", Fore.RESET, *args, sep='')