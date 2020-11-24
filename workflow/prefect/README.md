# Simple examples of using Prefect together with Dask

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

Once the Dask cluster is running, the scheduler address can be provided to
Prefect flow.


