from prefect import task, Task, Flow
import inspect

# API matching with type annotations

@task
def task1(a : int) -> float:
    return a

@task
def task2(b : int) -> float:
    return b

@task
def task3(c : float) -> float:
    return c

with Flow('api-test') as flow:
    r1 = task1(4)
    r2 = task2(r1)
    r3 = task3(r2)

# Check API matching
for task in flow:
    upstream = flow.upstream_tasks(task)
    if upstream:
        # How to deal with multiple upstream tasks ?
        upstream = upstream.pop()
        out_sig = inspect.signature(upstream.run)
        in_sig = inspect.signature(task.run)
        match = [param.annotation for param in in_sig.parameters.values()][0] == out_sig.return_annotation
        print("Matching of task {} to {} : {} ".format(upstream, task, match))

