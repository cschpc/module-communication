# Simple examples of using Prefect together with Dask

## Install

The necessary Python worker for Prefect core engine and Dask can be installed
with `pip`:
```
pip install -r requirements.txt
```

A singularity container can be build with
```
sudo singularity build prefect.simd prefect.def
```

## Creating a Dask cluster

Dask cluster can be started as follows. First central scheduler:
```bash
dask-scheduler
```
In the output, scheduler address and port are printed out.
Next, one or more workers can be started. If workers run on different host
than the scheduler, open network connection is needed. Also, an open network
connection between `workers` is needed.
```bash
dask-worker tcp://somehost:someport
```
It is also possible to provide a name and resources for the worker:
```
dask-worker tcp://somehost:someport --name MyName --resources "GPU=4"
```

## Prefect

Flow can be executed either locally or in the Dask cluster. In order to use
Dask the scheduler address needs be provided to Prefect flow. Flow can be
started in any machine that can access the scheduler.

Note: the `matrix_diagonalization_exes.py` which launches external programs
uses quick and dirty tricks for handling tasks with different number of
arguments.
