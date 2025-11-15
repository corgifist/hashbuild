from .compiler import *
from .linker import *
from .scheduler import *

def invoke_toolchain(files: list[str] | list[Path] | str,  output: str, binary_type: str, cxx: bool = False,
               compiler_flags: list[str] = [], linker_flags: list[str] = []) -> int:
    if type(files) is list[Path]:
        files = list(map(str, files))
    linker = schedule_linker(output=f"{get_build_path()}/{output}", flags=linker_flags)
    for file in files:
        id = schedule_compiler(linker, input=file, output=None, cxx=cxx, flags=compiler_flags)
        get_task_by_id(linker).wait_ids.append(id)
    
    return linker
    

def executable(files: list[str] | list[Path] | str, output: str, cxx: bool = False, 
               compiler_flags: list[str] = [], linker_flags: list[str] = []) -> None:
    return invoke_toolchain(files, output, 'executable', cxx, compiler_flags, linker_flags)
