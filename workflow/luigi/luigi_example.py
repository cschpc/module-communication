import luigi
from luigi_utilities import  LocalPythonTask, LocalShellTask, RemoteShellTask, RemoteSlurmTask
import os
from time import sleep

class Input(luigi.ExternalTask):

    def output(self):
        return luigi.LocalTarget('input.txt')


class Task1(LocalShellTask):

    remove_input = False
    exe = './exe1'

    def requires(self):
        return Input()


class Task2(RemoteSlurmTask):

    remove_input = False
    exe = './exe2'

    def requires(self):
        return Task1()

class Task3(RemoteShellTask):

    remove_input = False
    exe = './exe3'

    def requires(self):
        return Task1()

class Task4(LocalPythonTask):

    def requires(self):
        return [Task3(), Task2()]

    def output(self):
        return luigi.LocalTarget('final_output.txt')

    def run(self):

        data = []
        for inp in self.input():
            with inp.open('r') as f:
               data.extend([int(i) for i in f.readline().split()])

        data.append(data[-1] + 1)
        sleep(2)

        with self.output().open('w') as f:
            f.write(' '.join(map(str, data)))


if __name__ == '__main__':
    luigi.configuration.add_config_path('config.cfg')
    log_level = 'DEBUG' # default
    # log_level = 'INFO' # Less output
    luigi.build([Task4()], local_scheduler=True, log_level=log_level)
