! Preprocessor definitions
! Centered, backward and forward index for the x-dimension
#define ix      2:(x_dim-1)
#define ix_m    1:(x_dim-2)
#define ix_p    3:x_dim
! Centered, backward and forward index for the y-dimension
#define iy      2:(y_dim-1)
#define iy_m    1:(y_dim-2)
#define iy_p    3:y_dim

! Usage from Python:
! step_upwind(dx, dy, dt, u, v, C)
subroutine step_upwind(dx, dy, dt, u, v, C, C_new, x_dim, y_dim)
    implicit none
    ! Arguments
    integer                 :: x_dim, y_dim
    real, intent(in)        :: dx, dy, dt
    real, intent(in)        :: C(x_dim, y_dim), u(x_dim, y_dim), v(x_dim, y_dim)
    real, intent(out)       :: C_new(x_dim, y_dim)

    ! Local variables
    real, dimension(x_dim - 2, y_dim - 2) :: x_term, y_term

    !---------------
    ! Begin program
    !---------------

    x_term(:,:) = (&
        MAX(u(ix,iy), 0.) * (C(ix,iy) - C(ix_m,iy)) +&
        MIN(u(ix,iy), 0.) * (C(ix_p,iy) - C(ix,iy)) &
        )/dx

    y_term(:,:) = (&
        MAX(v(ix,iy), 0.) * (C(ix,iy) - C(ix,iy_m)) +&
        MIN(v(ix,iy), 0.) * (C(ix,iy_p) - C(ix,iy)) &
        )/dy

    C_new(ix,iy) = -(x_term + y_term)*dt + C(ix,iy)

end subroutine

! Usage from Python:
! step_leapfrog(dx, dy, dt, u, v, C)
subroutine step_leapfrog(dx, dy, dt, u, v, C, x_dim, y_dim)
    implicit none
    ! Arguments
    integer                 :: x_dim, y_dim
    real, intent(in)        :: dx, dy, dt
    real, intent(in)        :: u(x_dim, y_dim), v(x_dim, y_dim)
    real, intent(inout)     :: C(x_dim, y_dim, 2)
    !f2py intent(in,out)    :: C

    ! Local variabless
    real                    :: C_new(x_dim, y_dim)

    !---------------
    ! Begin program !
    !---------------

    ! Initialize only the boundaries
    C_new(:,1) = 0.
    C_new(:,y_dim) = 0.
    C_new(1,:) = 0.
    C_new(x_dim,:) = 0.

    ! Step
    C_new(ix,iy) = (                                                           &
        - u(ix,iy) * ( C(ix_p,iy,2) - C(ix_m,iy,2) ) / (2 * dx)                &
        - v(ix,iy) * ( C(ix,iy_p,2) - C(ix,iy_m,2) ) / (2 * dy)                &
        ) * 2 *dt + C(ix,iy,1)

    ! Switch out the old result
    C(:,:,1) = C(:,:,2)
    C(:,:,2) = C_new

end subroutine
