from .compiler import *
from .linker import *
from .scheduler import *

allow_static_libraries_for_osx = False

class InHouseLibraryPromise:
    def __init__(self, path, linker_id):
        self.path = path
        self.linker_id = linker_id

def invoke_toolchain(files: list[str] | list[Path] | str, output: str, binary_type: str, cxx: bool = False, definitions: dict[str, str] = {},
               libraries: list = [], compiler_flags: list[str] = [], linker_flags: list[str] = []) -> int:
    if binary_type != 'executable' and binary_type != 'shared' and binary_type != 'static':
        error(f'invalid binary type {binary_type}')
        exit(1)
    if type(files) is list[Path]:
        files = list(map(str, files))
    if type(files) is str:
        files = [files]
    if type(libraries) is not list:
        libraries = [libraries]
    linker = schedule_linker(output=f"{get_build_path()}/{output}", flags=linker_flags, libraries=libraries, cxx=cxx, binary_type=binary_type)
    for (index, library) in enumerate(libraries):
        if type(library) is InHouseLibraryPromise:
            libraries[index] = path.abspath(str(get_build_path()) + '/' + library.path)
            tasks[linker].wait_ids.append(library.linker_id)
    for file in files:
        id = schedule_compiler(linker, input=file, output=None, cxx=cxx, flags=compiler_flags, definitions=definitions)
        tasks[linker].wait_ids.append(id)

    if binary_type == 'static' or binary_type == 'shared':
        return InHouseLibraryPromise(
            f'{output}',
            linker
        )
    return linker
    

def executable(files: list[str] | list[Path] | str, output: str, cxx: bool = False, libraries: list = [],
               definitions: dict[str, str] = {}, compiler_flags: list[str] = [], linker_flags: list[str] = []) -> None:
    return invoke_toolchain(files=files, output=output, binary_type='executable', cxx=cxx, definitions=definitions,
                            libraries=libraries, compiler_flags=compiler_flags, linker_flags=linker_flags)

def library(files: list[str] | list[Path] | str, output: str, type: str = 'shared', cxx: bool = False, 
               definitions: dict[str, str] = {}, compiler_flags: list[str] = [], linker_flags: list[str] = []) -> InHouseLibraryPromise:
    # OSX requires static libraries to be linked ONLY with other static libraries
    # which means we can't link with standard library
    # for convenience purposes, static libraries on OSX are disabled
    if platform.system() == 'Darwin' and not allow_static_libraries_for_osx:
        type = 'shared'
    base_dir = path.dirname(output)
    base_name = path.basename(output)
    output = f'{base_dir}{get_library_name(base_name, library_type=type)}'
    return invoke_toolchain(files=files, output=output, binary_type=type, cxx=cxx, definitions=definitions,
                            compiler_flags=compiler_flags, linker_flags=linker_flags)