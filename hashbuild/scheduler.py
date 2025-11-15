from .compiler import *
from .linker import *
import atexit

class Task:
    def __init__(self, id: int, pipe_id: int = -1, wait_ids: list[int] = None, ready: bool = False):
        self.id = id
        self.pipe_id = pipe_id
        self.wait_ids = wait_ids if wait_ids is not None else list()
        self.ready = ready

    def print(self):
        info(f"running task {id}")

    def run(self):
        pass

global_task_id = -1
def gen_task_id():
    global global_task_id
    global_task_id += 1
    return global_task_id

tasks: list[Task] = []

def pipe_to_task(id: int, value: any) -> None:
    if id < 0:
        return
    tasks[id].pipe(value)

class CompilerTask(Task):
    def __init__(self, args, linker_id):
        super().__init__(gen_task_id(), pipe_id=linker_id)
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
        info(f"linking {'executable' if self.args['binary_type'] == 'executable' else self.args['binary_type'] + ' library'} {self.args['output']}")

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

def walk_child_tasks(task):
    for wait_id in task.wait_ids:
        wait_task = tasks[wait_id]
        if wait_task is None:
            continue
        if wait_task.ready:
            continue
        walk_child_tasks(wait_task)
        run_task(wait_task)

def dump_task(task: Task):
    info(task.id, '->', task.wait_ids)

def dump_orchestrator():
    info('orchestrator tree overview:')
    for task in tasks:
        dump_task(task)

def dispatch():
    for (id, _) in enumerate(tasks):
        task = tasks[id]
        if task.ready:
            continue
        walk_child_tasks(task)     
        run_task(task)


atexit.register(dispatch)