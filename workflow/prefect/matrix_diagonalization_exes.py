import prefect
from prefect import Task, Flow
from prefect.engine.results import LocalResult
from prefect.engine.executors import DaskExecutor
from subprocess import Popen, PIPE

import numpy as np

class MyShellTask(Task):
    def __init__(self, command, **kwargs):
        super().__init__(**kwargs)
        self.command = command

    def run(self, **kwargs):
        output_stream = kwargs.pop('output', None)
        command_args = kwargs.pop('args', [])
        if not isinstance(command_args, (tuple, list)):
            command_args = [command_args]

        # Ugly hack to ensure ordering of arguments
        input_stream = kwargs.pop('x', b'') + kwargs.pop('y', b'')
                                
        cmd = [self.command]
        cmd += [str(arg) for arg in command_args]

        with Popen(cmd, stdin=PIPE, stdout=output_stream) as p:
            s, err = p.communicate(input=input_stream)
            p.wait()
            if p.returncode:
                msg = "Command {} failed with exit code {}".format(
                    self.command, p.returncode)
                raise prefect.engine.signals.FAIL(msg)

        if output_stream == PIPE:
            return s

gen_diag_task = MyShellTask('generate_diag.py', name='gen_D')
gen_random_task = MyShellTask('generate_random.py', name='gen_ran')
qr_task = MyShellTask('qr.py', name='QR')
first_half_task = MyShellTask('first_half.py', name='first_half')
second_half_task = MyShellTask('second_half.py', name='second_half')
diag_task = MyShellTask('diagonalize.py', name='diagonalize', tags=["dask-resource:GPU=1"])
check_task = MyShellTask('check_results.py', name='check')
    
with Flow("numpy-example") as flow:
    D = gen_diag_task(output=PIPE, args=1000)
    A = gen_random_task(output=PIPE, args=1000)
    Q = qr_task(x=A, output=PIPE)
    B = first_half_task(x=D, y=Q, output=PIPE)
    C = second_half_task(x=Q, y=B, output=PIPE)
    eigvals = diag_task(x=C, output=PIPE)
    check_task(x=eigvals)

# dask_scheduler = 'tcp://somehost:someport'
# executor = DaskExecutor(address=dask_scheduler)
# flow_state = flow.run(executor=executor)
flow_state = flow.run()
