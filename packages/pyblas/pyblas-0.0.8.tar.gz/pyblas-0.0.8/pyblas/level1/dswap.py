# > \brief \b DSWAP
#
#  =========== DOCUMENTATION ===========
#
# Online html documentation available at
#            http://www.netlib.org/lapack/explore-html/
#
#  Definition:
#  ===========
#
#       def DSWAP(N,DX,INCX,DY,INCY)
#
#       .. Scalar Arguments ..
#       INTEGER INCX,INCY,N
#       ..
#       .. Array Arguments ..
#       DOUBLE PRECISION DX(*),DY(*)
#       ..
#
#
# > \par Purpose:
#  =============
# >
# > \verbatim
# >
# >    DSWAP interchanges two vectors.
# >    uses unrolled loops for increments equal to 1.
# > \endverbatim
#
#  Arguments:
#  ==========
#
# > \param[in] N
# > \verbatim
# >          N is INTEGER
# >         number of elements in input vector(s)
# > \endverbatim
# >
# > \param[in,out] DX
# > \verbatim
# >          DX is DOUBLE PRECISION array, dimension ( 1 + ( N - 1 )*abs( INCX ) )
# > \endverbatim
# >
# > \param[in] INCX
# > \verbatim
# >          INCX is INTEGER
# >         storage spacing between elements of DX
# > \endverbatim
# >
# > \param[in,out] DY
# > \verbatim
# >          DY is DOUBLE PRECISION array, dimension ( 1 + ( N - 1 )*abs( INCY ) )
# > \endverbatim
# >
# > \param[in] INCY
# > \verbatim
# >          INCY is INTEGER
# >         storage spacing between elements of DY
# > \endverbatim
#
#  Authors:
#  ========
#
# > \author Univ. of Tennessee
# > \author Univ. of California Berkeley
# > \author Univ. of Colorado Denver
# > \author NAG Ltd.
#
# > \date November 2017
#
# > \ingroup double_blas_level1
#
# > \par Further Details:
#  =====================
# >
# > \verbatim
# >
# >     jack dongarra, linpack, 3/11/78.
# >     modified 12/3/93, array(1) declarations changed to array(*)
# > \endverbatim
# >
#  =====================================================================
def DSWAP(N, DX, INCX, DY, INCY):
    #
    #  -- Reference BLAS level1 routine (version 3.8.0) --
    #  -- Reference BLAS is a software package provided by Univ. of Tennessee,    --
    #  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
    #     November 2017
    #
    #     .. Scalar Arguments ..
    # INTEGER INCX,INCY,N
    #     ..
    #     .. Array Arguments ..
    # DOUBLE PRECISION DX(*),DY(*)
    #     ..
    #
    #  =====================================================================
    #
    #     .. Local Scalars ..
    # DOUBLE PRECISION DTEMP
    # INTEGER I,IX,IY,M,MP1
    #     ..
    #     .. Intrinsic Functions ..
    # INTRINSIC MOD
    #     ..
    if N <= 0:
        return
    if INCX == 1 and INCY == 1:
        #
        #       code for both increments equal to 1
        #
        #
        #       clean-up loop
        #
        M = N % 3
        if M != 0:
            for I in range(M):
                DTEMP = DX[I]
                DX[I] = DY[I]
                DY[I] = DTEMP
            if N < 3:
                return
        for I in range(M, N, 3):
            DTEMP = DX[I]
            DX[I] = DY[I]
            DY[I] = DTEMP
            DTEMP = DX[I + 1]
            DX[I + 1] = DY[I + 1]
            DY[I + 1] = DTEMP
            DTEMP = DX[I + 2]
            DX[I + 2] = DY[I + 2]
            DY[I + 2] = DTEMP
    else:
        #
        #       code for unequal increments or equal increments not equal
        #         to 1
        #
        IX = 1
        IY = 1
        if INCX < 0:
            IX = (-N + 1) * INCX + 1
        if INCY < 0:
            IY = (-N + 1) * INCY + 1
        for I in range(N):
            DTEMP = DX[IX]
            DX[IX] = DY[IY]
            DY[IY] = DTEMP
            IX += INCX
            IY += INCY
