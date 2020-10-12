import time
from subprocess import Popen
import zmq
import numpy as np
import yaml
from utility import init_sockets, send_array, recv_array


port_0 = 5557
my_destination = 'tcp://127.0.0.1:{}'.format(port_0)

# Read pipeline configuration
with open('conf.yaml') as f: 
    conf = yaml.load(f, Loader=yaml.SafeLoader)


modules = conf['pipeline']
args = []
source_port = port_0
for m in modules:
    source = 'tcp://127.0.0.1:{}'.format(source_port)
    source_port += 1
    destination = 'tcp://127.0.0.1:{}'.format(source_port)
    args.append((source, destination))

my_source = 'tcp://127.0.0.1:{}'.format(source_port)

receiver, sender = init_sockets(my_source, my_destination)

processes = []
for m, a in zip(modules, args):
    launcher = './'
    try:
        module_conf = conf[m]
        for c in module_conf:
            if 'launcher' in c:
                launcher = c['launcher']
    except KeyError:
        pass
    cmd = launcher + m + ' ' + ' '.join(a)
    print("Starting process", cmd)
    processes.append(Popen(cmd, shell=True))

send_array(sender, np.array((10)))
final_result = recv_array(receiver)
print("Master: ", final_result)

while True:
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        print()
        break

print("Workflow finished")
