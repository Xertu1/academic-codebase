module GLOBAL
    use iso_fortran_env, only : real64
    implicit none
    integer, parameter :: n = 10
    integer, parameter :: m = 9
end module GLOBAL

module READFILE
    use iso_fortran_env, only : real64
    use GLOBAL
    implicit none
    real(real64), dimension(n,n,m) :: A
    real(real64), dimension(n,m) :: vrh
    real(real64), dimension(m) :: conds
    real(real64), dimension(n) :: exact_solution
    character(len=*), parameter :: data_dir = '../data/'
contains
    subroutine matrix_read()
        integer :: io, i, j, k
        character(len=64) :: matrix_name

        do k = 1, m
            write(matrix_name, '(a,"matrix",i0,".txt")') trim(data_dir), k
            open(newunit=io, file=trim(matrix_name), status='old', action='read')
            do i = 1, n
                read(io, *) (A(i,j,k), j = 1, n)
            end do
            close(io)
        end do
    end subroutine matrix_read

    subroutine conds_read()
        integer :: io, k, ios
        character(len=128) :: line

        open(newunit=io, file=trim(data_dir)//'conds.txt', status='old', action='read')
        do k = 1, m
            do
                read(io, '(A)', iostat=ios) line
                if (ios /= 0) exit
                if (len_trim(line) == 0) cycle
                read(line, *) conds(k)
                exit
            end do
        end do
        close(io)
    end subroutine conds_read

    subroutine solution_read()
        integer :: io, i

        open(newunit=io, file=trim(data_dir)//'solution.txt', status='old', action='read')
        do i = 1, n
            read(io, *) exact_solution(i)
        end do
        close(io)
    end subroutine solution_read

    subroutine vrh_read()
        integer :: io, k, i

        open(newunit=io, file=trim(data_dir)//'vector righ half.txt', status='old', action='read')
        do k = 1, m
            do i = 1, n
                read(io, *) vrh(i,k)
            end do
        end do
        close(io)
    end subroutine vrh_read
end module READFILE

module JORDAN
    use iso_fortran_env, only : real64
    use GLOBAL
    implicit none
contains
    subroutine jordan(Ain, b, x)
        real(real64), intent(in) :: Ain(n,n)
        real(real64), intent(in) :: b(n)
        real(real64), intent(out) :: x(n)
        real(real64) :: aug(n,n+1), pivot, factor
        integer :: i, k

        aug(:,1:n) = Ain
        aug(:,n+1) = b

        do k = 1, n
            pivot = aug(k,k)
            if (pivot == 0.0_real64) then
                stop 'Zero pivot encountered in jordan'
            end if
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

module RESEARCH
    use iso_fortran_env, only : real64
    use GLOBAL
    implicit none
contains
    subroutine write_actual_errors(solutions, exact, path)
        real(real64), intent(in) :: solutions(n,m)
        real(real64), intent(in) :: exact(n)
        character(len=*), intent(in) :: path
        real(real64) :: err(n)
        integer :: io, k

        open(newunit=io, file=path, status='replace', action='write')
        do k = 1, m
            err = abs(solutions(:,k) - exact)
            write(io, '(*(es24.16,1x))') err
            if (k < m) write(io, *)
        end do
        close(io)
    end subroutine write_actual_errors
end module RESEARCH

program main
    use iso_fortran_env, only : real64
    use GLOBAL
    use READFILE
    use JORDAN
    use RESEARCH
    implicit none
    real(real64), dimension(n,m) :: solutions
    real(real64), dimension(m) :: timings
    real(real64) :: t_start, t_end
    integer :: k, io

    call matrix_read()
    call vrh_read()
    call solution_read()
    call conds_read()

    do k = 1, m
        call cpu_time(t_start)
        call jordan(A(:,:,k), vrh(:,k), solutions(:,k))
        call cpu_time(t_end)
        timings(k) = t_end - t_start
    end do

    open(newunit=io, file='../data/computed_solutions.txt', status='replace', action='write')
    do k = 1, m
        write(io, '(*(es24.16,1x))') solutions(:,k)
        if (k < m) write(io, *)
    end do
    close(io)

    call write_actual_errors(solutions, exact_solution, '../data/actual_errors.txt')

    open(newunit=io, file='../data/execution_times.txt', status='replace', action='write')
    do k = 1, m
        write(io, '(es24.16)') timings(k)
    end do
    close(io)
end program main
