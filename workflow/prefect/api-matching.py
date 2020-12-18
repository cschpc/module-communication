# Simple ideas for checking whether tasks can be combined
# In real use case one should traverse the flow and handle also the case where
# task depends on multiple upstream tasks


from prefect import task, Task
import inspect

@task
def task1(a : int) -> float:
    return a

@task
def task2(b : int) -> float:
    return b

@task
def task3(c : float) -> float:
    return c

sig1 = inspect.signature(task1.run)
sig2 = inspect.signature(task2.run)
sig3 = inspect.signature(task3.run)

match = [param.annotation for param in sig2.parameters.values()][0] == sig1.return_annotation
print("Matching of task1 to task2: ", match)
match = [param.annotation for param in sig3.parameters.values()][0] == sig2.return_annotation
print("Matching of task2 to task3: ", match)


class MyTask1(Task):

   def input_api(self):
       return "foo"

   def output_api(self):
       return "bar"

class MyTask2(Task):

   def input_api(self):
       return "foo2"

   def output_api(self):
       return "bar2"

class MyTask3(Task):

   def input_api(self):
       return "bar2"

   def output_api(self):
       return "bar3"

task1 = MyTask1()
task2 = MyTask2()
task3 = MyTask3()

print("Matching of task1 to task2: ", task2.input_api() == task1.output_api())
print("Matching of task3 to task2: ", task3.input_api() == task2.output_api())


