! Usage from Python:
! step_advection(dx, dt, u, C_now)
! Parameters x_dim and C_new are not passed explicitly through a function call
subroutine step_upwind(dx, dy, dt, u, v, C, C_new, x_dim, y_dim)
    !!!!!!!!!!!!
    ! Preamble !
    !!!!!!!!!!!!  
    implicit none 

    ! Arguments 
    integer                 :: x_dim, y_dim 
    double precision, intent(in)        :: dx, dy, dt
    double precision, intent(in)        :: C(x_dim, y_dim), u(x_dim, y_dim), v(x_dim, y_dim)
    double precision, intent(out)       :: C_new(x_dim, y_dim) 
    double precision                    :: term1, term2

    ! Local variables 
    integer                 :: i, j

    !!!!!!!!!!!!!!!!!!
    ! Begin function !
    !!!!!!!!!!!!!!!!!!

    ! Set boundaries to zero
    do i = 1, x_dim
        C_new(i, 1) = 0
        C_new(i, y_dim) = 0
    end do
    do j = 1, y_dim
        C_new(1, j) = 0
        C_new(x_dim, j) = 0
    end do 

    ! Loop over the array and find a new C value for each element
    do i = 2, x_dim - 2
        do j = 2, y_dim - 2 
            IF (u(i,j) .GT. 0) THEN !FTBS 
                term1 = v(i,j) * (C(i,j) - C(i-1,j))/dx
            ELSE                    !FTFS 
                term1 = v(i,j) * (C(i+1,j) - C(i,j))/dx
            END IF

            IF (v(i,j) .GT. 0) THEN !FTBS
                term2 = u(i,j) * (C(i,j) - C(i,j-1))/dy
            ELSE                    !FTFS
                term2 = u(i,j) * (C(i,j+1) - C(i,j))/dy
            END IF 

            C_new(i,j) = (-term1 - term2)*dt + C(i,j)
        end do
    end do 

end subroutine 

subroutine step_leapfrog(dx, dy, dt, u, v, C, x_dim, y_dim)
    !!!!!!!!!!!!
    ! Preamble !
    !!!!!!!!!!!!  
    implicit none 

    ! Arguments 
    integer                 :: x_dim, y_dim 
    real, intent(in)        :: dx, dy, dt
    real, intent(in)        :: u(x_dim, y_dim), v(x_dim, y_dim)
    double precision, intent(inout)     :: C(x_dim, y_dim, 2) 
    !f2py intent(in,out) :: C(x_dim, y_dim, 2)
    double precision                    :: C_new(x_dim, y_dim) 

    ! Local variables 
    integer                 :: i, j

    !!!!!!!!!!!!!!!!!!
    ! Begin function !
    !!!!!!!!!!!!!!!!!!

    ! Set boundaries to zero
    do i = 1, x_dim
        C_new(i, 1) = 0
        C_new(i, y_dim) = 0
    end do
    do j = 1, y_dim
        C_new(1, j) = 0
        C_new(x_dim, j) = 0
    end do 

    ! Step forward
    do i = 2, x_dim - 1
        do j = 2, x_dim - 1
            C_new(i,j) = ( -v(i,j)*(C(i+1,j,2) - C(i-1,j,2))/(2*dx) -&
                u(i,j)*(C(i,j+1,2) - C(i,j-1,2))/(2*dy) )*2*dt + C(i,j,1)
        end do
    end do

    ! Apply filter
    !C_new(:,:) = C(:,:,2) + 0.05/2.0*(C_new(:,:) - 2*C(:,:,2) + C(:,:,1))

    ! Switch out the old result
    C(:,:,1) = C(:,:,2)
    C(:,:,2) = C_new 
end subroutine
