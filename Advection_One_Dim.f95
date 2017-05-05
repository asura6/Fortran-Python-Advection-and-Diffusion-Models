! Preprocessor definitions
! Indexes used by the numerical schemes
#define ix      2:x_dim
#define ix_m    1:(x_dim-1)
#define ix_c    2:(x_dim-1)
#define ix_cp   3:x_dim
#define ix_cm   1:(x_dim-2)

! Usage from Python:
! step_advection(dx, dt, u, C)
subroutine step_ftbs(dx, dt, u, C, x_dim)
    implicit none
    ! Arguments
    integer                 :: x_dim
    real, intent(in)        :: dx, dt
    real, intent(in)        :: u(x_dim)
    real, intent(inout)     :: C(x_dim)
    !f2py intent(in,out)    :: C

    !---------------
    ! Begin program
    !---------------

    C(ix) = dt * ( -u(ix)* (C(ix)-C(ix_m)) - C(ix) * (u(ix)-u(ix_m)) ) *       &
        dt/dx + C(ix)

end subroutine

! Usage from Python:
! step_ftbs_diffusion(dx, dt, u, D, C)
subroutine step_ftbs_diffusion(dx, dt, u, D, C, x_dim)
    implicit none
    ! Arguments
    integer                 :: x_dim
    real, intent(in)        :: dx, dt, D
    real, intent(in)        :: u(x_dim)
    real, intent(inout)     :: C(x_dim)
    !f2py intent(in,out)    :: C

    !---------------
    ! Begin program
    !---------------

    C(ix_c) = D * ( (C(ix_cp) -2*C(ix_c) + C(ix_cm))/dx**2                     &
        - u(ix_c) * (C(ix_c) - C(ix_cm))/dx ) * dt + C(ix_c)

end subroutine
