from .compiler import *
from .linker import *
import atexit

class Task:
    def __init__(self, id: int, pipe_id: int = -1, wait_ids: list[int] = [], ready: bool = False):
        self.id = id
        self.pipe_id = pipe_id
        self.wait_ids = wait_ids
        self.ready = False

    def print(self):
        info(f"running task {id}")

global_task_id = 0
def gen_task_id():
    global global_task_id
    global_task_id += 1
    return global_task_id

tasks: list[Task] = []

def get_task_by_id(id: int) -> Task:
    for task in tasks:
        if task.id == id:
            return task
        
    return None

def pipe_to_task(id: int, value: any) -> None:
    task = get_task_by_id(id)
    if task is not None:
        task.pipe(value)

class CompilerTask(Task):
    def __init__(self, args, linker_id):
        super().__init__(gen_task_id(), linker_id)
        self.args = args
    
    def print(self):
        info(f"compiling file {self.args['input']}")

    def run(self):
        pipe_to_task(self.pipe_id, compile_file(**self.args))

class LinkerTask(Task):
    def __init__(self, args):
        super().__init__(gen_task_id())
        self.args = args
        self.objects = []
    
    def print(self):
        info(f"linking {self.args['output']}")

    def pipe(self, value):
        self.objects.append(value)

    def run(self):
        link_objects(**self.args, objects=self.objects)

def schedule_compiler(linker_id, **kwargs) -> int:
    task = CompilerTask(kwargs, linker_id)
    tasks.append(task)
    return task.id

def schedule_linker(**kwargs):
    task = LinkerTask(kwargs)
    tasks.append(task)
    return task.id

def run_task(task: Task):
    task.print()
    task.run()
    task.ready = True

def dispatch():
    for task in tasks:
        if task.ready:
            continue
        if len(task.wait_ids) > 0:
            for wait_id in task.wait_ids:
                wait_task = get_task_by_id(wait_id)
                if wait_task is not None:
                    run_task(wait_task)
        run_task(task)


atexit.register(dispatch)