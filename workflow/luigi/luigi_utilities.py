import luigi
from luigi.contrib.ssh import RemoteContext, RemoteTarget, RemoteFileSystem
import os
import subprocess

from time import sleep

# Basic model of Task in Luigi: a task is run after the Target(s)
# returned by the output() of required Task exist
class MyTask(luigi.Task):

    def requires(self):
        return OtherTask() # or return [OtherTask1(), OtherTask2()]

    def output(self):
        return SomeTarget()

    def run(self):
        # output of required Task available via self.input()
        # the Target of self.output() needs to be created 
        pass

class LocalPythonTask(luigi.Task):

    remove_input = True

    def process(self):
        raise NotImplementedError('subclass needs to implement process')

    def output(self):
        filename = 'tmp/tmp_{}.txt'.format(self.__class__.__name__)
        return luigi.LocalTarget(filename)

    def run(self):
        with self.input().open('r') as f:
            # read input
            inp_data = f.readline().strip()

        result = self.process(inp_data)

        with self.output().open('w') as f:
            f.write(result)      

        # clean up intermediate files
        if self.remove_input:
            self.input().remove()

class LocalShellTask(luigi.Task):
    """Executes an external binary

    exe input_file output_file

    Binary need to exist in PATH"""

    remove_input = True
    exe = luigi.Parameter()

    def output(self):
        filename = 'tmp/tmp_{}.txt'.format(self.__class__.__name__)
        return luigi.LocalTarget(filename)

    def run(self):
        # Remote targets need to be copied first
        inp = self.input()
        if isinstance(inp, RemoteTarget):
            inp.get(inp.path)            
        infile = inp.path
        outfile = self.output().path
        subprocess.run([self.exe, infile, outfile])

        # clean up intermediate files
        if isinstance(inp, RemoteTarget):
            os.remove(infile)

        if self.remove_input:
            self.input().remove()


class RemoteShellTask(luigi.Task):
    """Executes an external binary in remote system via ssh

    exe input_file output_file
    
    Input is copied to remote system, output is created as remote target
    
    Binary need to exist in PATH in the remote system"""

    remove_input = True
    exe = luigi.Parameter()
    remote_dir = luigi.Parameter()
    ssh_host = luigi.Parameter()

    def output(self):
        remote_path = os.path.join(self.remote_dir, 'remote_out.txt')
        return RemoteTarget(path=remote_path, host=self.ssh_host)

    def run(self):
        # copy input to remote host
        # Remote targets need to be copied first to local system
        inp = self.input()
        if isinstance(inp, RemoteTarget):
            inp.get(inp.path)            

        remote_fs = RemoteFileSystem(self.ssh_host)
        remote_path = os.path.join(self.remote_dir, self.input().path)
        remote_fs.put(self.input().path, remote_path)

        infile = self.input().path
        outfile = os.path.basename(self.output().path)

        remote = RemoteContext(self.ssh_host)
        remote.check_output(['cd {};'.format(self.remote_dir),
                              self.exe, infile, outfile])

        # clean up intermediate files
        if isinstance(inp, RemoteTarget):
            os.remove(infile)
            
        remote_fs.remove(remote_path)

        if self.remove_input:
            self.input().remove()

class RemoteSlurmTask(luigi.Task):
    """Executes an external binary in remote system with Slurm

    exe input_file output_file
    
    Input is copied to remote system, output is created as remote target
    
    Binary need to exist in PATH in the remote system"""

    slurm_time = '00:05:00'
    slurm_partition = 'test'
    remote_dir = luigi.Parameter()
    ssh_host = luigi.Parameter()

    def output(self):
        remote_path = os.path.join(self.remote_dir, 'remote_out.txt')
        return RemoteTarget(path=remote_path, host=self.ssh_host)

    def run(self):

        # copy input to remote host
        # Remote targets need to be copied first to local system
        inp = self.input()
        if isinstance(inp, RemoteTarget):
            inp.get(inp.path)            

        remote_fs = RemoteFileSystem(self.ssh_host)
        remote_path = os.path.join(self.remote_dir, self.input().path)
        remote_fs.put(self.input().path, remote_path)

        infile = self.input().path
        outfile = os.path.basename(self.output().path)

        # create slurm batch script
        with open('slurm_job.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('#SBATCH --job-name=luigi-task\n')
            f.write('#SBATCH --time={}\n'.format(self.slurm_time))
            f.write('#SBATCH --partition={}\n'.format(self.slurm_partition))
            f.write('#SBATCH --ntasks=1\n')
            f.write('#SBATCH --account=project_2002078\n')
            f.write('\n')
            f.write('srun {} {} {}\n'.format(self.exe, infile, outfile))
            f.write('\n')

        # copy batch script to remote host
        remote_path = os.path.join(self.remote_dir, 'slurm_job.sh')
        remote_fs.put('slurm_job.sh', remote_path)
        os.remove('slurm_job.sh')

        # Submit batch job and wait for its completion
        remote = RemoteContext(self.ssh_host)
        slurm_out = remote.check_output(['cd {};'.format(self.remote_dir), 'sbatch', 'slurm_job.sh'])
        job_id = int(slurm_out.split()[-1])
        sacct_cmd = 'sacct -n -X -j {}'.format(job_id)
        # Wait for job to complete
        sleep(20)
        while True:
            sacct_out = remote.check_output([sacct_cmd]).decode('utf-8')
            if 'COMPLETED' in sacct_out:
                print("DEB: completed")
                break
            elif 'FAILED' in sacct_out:
                self.output().remove()
                raise RuntimeError('Task {} failed'.format(self.__class__.__name__))
            else:
                # Do not poll sacct too frequently
                sleep(60)
