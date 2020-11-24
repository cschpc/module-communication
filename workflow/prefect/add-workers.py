# Simple example for launching remote dask-workers 
# It is assumed that the scheduler is running on localhost

# Note that the port forwarding here is not enough for communicating **between** the workers


from subprocess import run

workers = {
    'dask2' : {'ip' : '1.2.3.4', 
               'resources' : 'GPU=1'
              },
    'dask1' : {'ip' : '1.2.3.5', 
               'resources' : 'light=1000'
              },
}

scheduler_port=8786

worker_port=8788
for name, info in workers.items():
    remote_forward = '-R{0}:localhost:{0}'.format(scheduler_port)
    local_forward = '-L{0}:localhost:{0}'.format(worker_port)
    host=info['ip']
    resources=info.setdefault('resources')
    cmd = ['ssh', '-f', remote_forward, local_forward, host,
           'dask-worker', 'tcp://localhost:{0}'.format(scheduler_port),
           '--worker-port', str(worker_port), '--name', name]
    if resources:
        cmd.append('--resources "{0}"'.format(resources))

    print(cmd)
    run(cmd)
    worker_port += 1


