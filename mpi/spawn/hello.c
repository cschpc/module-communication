#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>

int main(int argc, char *argv[])
{
    int i, myid, ntasks, nctasks, mycid, msg;
    int errors[4];
    MPI_Comm intra, inter;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &ntasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);


    if (myid == 0) {
        printf("In total there are %i C tasks\n", ntasks);
    }

    printf("Hello from C %i\n", myid);
    MPI_Comm_spawn("hello_f", MPI_ARGV_NULL, 4, MPI_INFO_NULL, 0, MPI_COMM_WORLD,
                    &inter, errors);

    MPI_Comm_size(inter, &nctasks);
    MPI_Comm_remote_size(inter, &ntasks);

    if (myid == 0) {
        printf("In total there are %i C tasks\n", nctasks);
        printf("In total there are %i F tasks\n", ntasks);
    }

    // msg = mycid + 100;
    // MPI_Send(&msg, 1, MPI_INT, mycid, 0, inter);


    MPI_Finalize();
    return 0;
}
