program ex1
  use mpi
  implicit none
  integer :: rc, myid, ntasks, nftasks, myfid, color
  integer(kind=MPI_ADDRESS_KIND) :: appnum, universe_size
  logical :: flag
  integer :: intra, inter, msg

  flag = .true.

  call MPI_INIT(rc)

  call MPI_COMM_SIZE(MPI_COMM_WORLD, ntasks, rc)
  call MPI_COMM_RANK(MPI_COMM_WORLD, myid, rc)

  call MPI_COMM_GET_ATTR(MPI_COMM_WORLD, MPI_UNIVERSE_SIZE, universe_size, &
                         flag, rc)
  call MPI_COMM_GET_ATTR(MPI_COMM_WORLD, MPI_APPNUM, appnum, &
                         flag, rc)
  if (.not. flag) then
     write(*,*) 'No MPI_APPNUM'
     color = 1
  else
     write(*,*) 'Appnum', appnum
     color = appnum
  end if

  ! call MPI_COMM_SPLIT(MPI_COMM_WORLD, color, myid, intra, rc)
  call MPI_COMM_SPLIT(MPI_COMM_WORLD, 22, myid, intra, rc)
  call MPI_COMM_SIZE(intra, nftasks, rc)
  call MPI_COMM_RANK(intra, myfid, rc)

  if(myfid == 0) then
     write(*,*) 'In total there are ', universe_size, ' tasks and ' ,nftasks, 'Fortran tasks'
  endif

  write(*,*) 'Hello from Fortran', myid

  call MPI_INTERCOMM_CREATE(intra, 0, MPI_COMM_WORLD, 0, 99, inter, rc)
  call MPI_RECV(msg, 1, MPI_INTEGER, myfid, 0, inter, MPI_STATUS_IGNORE, rc)
  write(*,*) 'Fortran rank', myfid, 'received', msg, 'from C'

  call MPI_FINALIZE(rc)

end program ex1
