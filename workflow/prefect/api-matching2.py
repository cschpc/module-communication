from prefect import task, Task, Flow
import inspect


# API matching with explicit methods

class MyTask1(Task):

   def run(self, a):
       pass

   def input_api(self):
       return "foo"

   def output_api(self):
       return "bar"

class MyTask2(Task):

   def run(self, a):
       pass

   def input_api(self):
       return "foo2"

   def output_api(self):
       return "bar2"

class MyTask3(Task):

   def run(self, a):
       pass

   def input_api(self):
       return "bar2"

   def output_api(self):
       return "bar3"


task1 = MyTask1()
task2 = MyTask2()
task3 = MyTask3()

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
        match = task.input_api() == upstream.output_api()
        print("Matching of task {} to {} : {} ".format(upstream, task, match))


