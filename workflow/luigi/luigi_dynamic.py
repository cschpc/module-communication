import luigi
import shutil
import subprocess

class LocalDynamicShellTask(luigi.Task):

  exes = luigi.ListParameter(default=[])
  file = luigi.Parameter('out.txt')

  def output(self):
    return luigi.LocalTarget(self.file)

  def run(self):
    exe_list = list(self.exes)

    if exe_list:
      exe = exe_list.pop()
      input = yield LocalTask(exes=exe_list)
      infile = input.path
      outfile = self.output().path
      subprocess.run([exe, infile, outfile])

    else:
      # Make input.txt the first target
      shutil.copy('input.txt', self.output().path)

if __name__ == '__main__':
  exes = ['./exe1', './exe2', './exe3']
  luigi.build([LocalDynamicShellTask(exes=exes)], local_scheduler=True)
