program ex1
  use mpi
  implicit none
  integer :: rc, myid, ntasks, nftasks, myfid
  integer :: intra, inter, msg

  call MPI_INIT(rc)

  call MPI_COMM_SIZE(MPI_COMM_WORLD, ntasks, rc)
  call MPI_COMM_RANK(MPI_COMM_WORLD, myid, rc)


  if(myid == 0) then
     write(*,*) 'In total there are ',ntasks, 'Fortran tasks'
  endif

  write(*,*) 'Hello from Fortran', myid

  ! call MPI_INTERCOMM_CREATE(intra, 0, MPI_COMM_WORLD, 0, 99, inter, rc)
  ! call MPI_RECV(msg, 1, MPI_INTEGER, myfid, 0, inter, MPI_STATUS_IGNORE, rc)
  ! write(*,*) 'Fortran rank', myfid, 'received', msg, 'from C'

  call MPI_FINALIZE(rc)

end program ex1
