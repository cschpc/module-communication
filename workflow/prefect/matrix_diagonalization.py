from prefect import task, Flow
from prefect.engine.executors import DaskExecutor

import numpy as np

@task
def generate_diag(n):
    eigvals = np.arange(0, n, dtype=float)
    D = np.diag(eigvals)
    return D

@task
def generate_random(n):
    A = np.random.random((n, n))
    return A

@task
def qr(A):
    Q, R = np.linalg.qr(A)
    return Q

@task 
def first_half(D, Q):
    B = np.matmul(D, Q.T)
    return B

@task
def second_half(Q, B):
    C = np.matmul(Q, B)
    return C

@task
def diagonalize(C):
    eigvals = np.linalg.eigvals(C)
    eigvals.sort()
    return eigvals

@task
def check_result(eigvals):
    n = len(eigvals)
    correct = np.arange(0, n, dtype=float)
    check = np.abs(eigvals - correct).max() < 0.0001
    print("Check results:", check)


with Flow("numpy-example") as flow:
    D = generate_diag(1000)
    A = generate_random(1000)
    Q = qr(A)
    B = first_half(D, Q)
    C = second_half(Q, B)
    eigvals = diagonalize(C)
    check_result(eigvals)

# dask_scheduler = 'tcp://somehost:someport'
# executor = DaskExecutor(address=dask_scheduler)
# flow_state = flow.run(executor=executor)
flow_state = flow.run()

