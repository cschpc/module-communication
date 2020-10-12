#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>

int main(int argc, char *argv[])
{
    int i, myid, ntasks, nctasks, mycid, color, msg;
    MPI_Comm intra, inter;
    int *appnum, *universe_size, flag;
    flag = 1;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &ntasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);

    MPI_Comm_get_attr(MPI_COMM_WORLD, MPI_UNIVERSE_SIZE, &universe_size, &flag); 
    MPI_Comm_get_attr(MPI_COMM_WORLD, MPI_APPNUM, &appnum, &flag); 
    if (!flag)
            printf("MPI_APPNUM is not provided\n");
    else
       printf("Appnum %i\n", *appnum);

    // MPI_Comm_split(MPI_COMM_WORLD, *appnum, myid, &intra);
    MPI_Comm_split(MPI_COMM_WORLD, 0, myid, &intra);
    MPI_Comm_size(intra, &nctasks);
    MPI_Comm_rank(intra, &mycid);

    if (mycid == 0) {
        printf("In total there are %i tasks and %i C tasks\n", 
               *universe_size, nctasks);
    }

    printf("Hello from C %i\n", myid);
    MPI_Intercomm_create(intra, 0, MPI_COMM_WORLD, ntasks / 2, 99, &inter);

    msg = mycid + 100;
    MPI_Send(&msg, 1, MPI_INT, mycid, 0, inter);


    MPI_Finalize();
    return 0;
}
