! Usage from Python:
! step_advection(dx, dt, u, C_now)
! Parameters x_dim and C_new are not passed explicitly through a function call
subroutine step_advection(dx, dt, u, C_now, C_new, x_dim)
    !!!!!!!!!!!!
    ! Preamble !
    !!!!!!!!!!!!  

    implicit none 

    ! Arguments 
    integer                 :: x_dim 
    real, intent(in)        :: dx, dt
    real, intent(in)        :: C_now(x_dim), u(x_dim)
    real, intent(out)       :: C_new(x_dim) 

    ! Local variables 
    integer                 :: i 

    !!!!!!!!!!!!!!!!!!
    ! Begin function !
    !!!!!!!!!!!!!!!!!!

    ! Set left boundary to zero
    C_new(1) = 0
    ! Loop over the array and find a new C value for each element
    do i = 2, x_dim
        C_new(i) = dt * ( -u(i) * (C_now(i) - C_now(i-1)) / dx - &
            C_now(i) * (u(i) - u(i-1)) / dx ) + &
            C_now(i)
    end do 

end subroutine

! Usage from Python:
! step_advection_diffusion(dx, dt, u, D, C_now)
! Parameters x_dim and C_new are not passed explicitly through a function call
subroutine step_advection_diffusion(dx, dt, u, D, C_now, C_new, x_dim)
    !!!!!!!!!!!!
    ! Preamble !
    !!!!!!!!!!!!  

    implicit none 

    ! Arguments 
    integer                 :: x_dim 
    real, intent(in)        :: dx, dt, D
    real, intent(in)        :: C_now(x_dim), u(x_dim)
    real, intent(out)       :: C_new(x_dim) 

    ! Local variables 
    integer                 :: i 

    !!!!!!!!!!!!!!!!!!
    ! Begin function !
    !!!!!!!!!!!!!!!!!!

    ! Set boundaries to zero
    C_new(1) = 0
    C_new(x_dim) = 0
    ! Loop over the array and find a new C value for each element
    do i = 2, x_dim - 1
        C_new(i) = (D*(C_now(i+1) - 2*C_now(i) + C_now(i-1)) &
            - u(i)*(C_now(i) - C_now(i-1))/dx)*dt + C_now(i)
    end do 
    return
end subroutine 
