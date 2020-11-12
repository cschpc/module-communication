# Simple Luigi example

## Installing luigi

(Within virtual environment if needed)
```
pip install luigi
```

## Usage

The module `luigi_utilities` contains templates for basic simple tasks
both for local and remote execution. The actual pipeline is defined in
`luigi_example.py` and can be run as:
```
python luigi_example.py
```
The "executables" `exe1`, `exe2`, `exe3` are actully dummy Python code
with a usage model:
```
./exeX input_file output_file
```

For remote execution, the
"executables" `exe2` and `exe3` need to be copied to proper remote
locations.

Remote systems can be specified in `config.cfg`

Pipeline branches and joins:
```
         Task1
        /     \
	   /       \
	Task2     Task3
	   \       /
	    \     /
		 Task4
```

Note! At the moment cleaning of intermediate files does not work with
branching pipelines. For reruns, the outputs in remote system need to
be cleaned out (=removed) manually.


