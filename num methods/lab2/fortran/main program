module GLOBAL
    implicit none
    integer :: n=10
end module GLOBAL

module READFILE
    use GLOBAL
    real, dimension(10,10,9) :: A
    real, dimension(10,9) :: vrh, cond
    implicit none
    contains
        subroutine matrix_read()
            integer :: io, i, j, k
            character(len=20) :: matrix_name

            do k =1,9
                write(matrix_name, '("matrix", i0, ".txt")') k
                open(newunit=io, file=matrix_name, status='old', action='read')
                    do i = 1, n
                        read(io,*) (A(i,j,k), j = 1, n)
                    end do
                close(io)
            end do
        end subroutine matrix_read

        subroutine conds_read()
            integer :: io, k
            
            open(newunit=io, file='conds.txt', status='old', action='read')
            do k=1,9
                read(io, *) cond(:,k)
                read(io,*)
            end do
            close(io)
        end subroutine conds_read

        subroutine solution_read()
            integer :: io, solution,k

            open(newunit=io, file='solution.txt', status='old', action='read')
            do k=1,10
                read(io,*) solution
            end do
            close (io)

        end subroutine solution_read

        subroutine vrh_read()
            integer :: io, k, i

            open(newunit=io, file='vector righ half.txt', status='old', action='read')
            do k = 1,9
                do i = 1, n
                    read(io, *) vrh(i,k)
                end do
                read(io, *)
            end do
            close(io)
        end subroutine vrh_read
end module READFILE

module JORDAN
    use GLOBAL
    implicit none
    contains
        subroutine jordan(Ain, b, x)
            implicit none
            real :: Ain(n,n), b(n)
            real :: x(n)
            real :: aug(n,n+1), pivot, factor
            integer :: i, j, k

            aug(:,1:n) = Ain
            aug(:,n+1) = b

            do k = 1, n
                pivot = aug(k,k)                     
                aug(k,1:n+1) = aug(k,1:n+1) / pivot 

                do i = 1, n
                    if (i /= k) then
                        factor = aug(i,k)
                        aug(i,1:n+1) = aug(i,1:n+1) - factor*aug(k,1:n+1)
                    end if
                end do
            end do
            x = aug(:,n+1)
        end subroutine jordan
end module JORDAN

program main
    use READFILE
    use GLOBAL
    use JORDAN
    implicit none

    call jordan(A(:,:,k), vrh(:,k), x, info)

end program main
