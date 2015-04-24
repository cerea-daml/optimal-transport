import utils_grid as grid
import utils_bound_constrain as cb
import utils_stag_cent_resbound_constrain as cscrb
import utils_stag_cent_tempbound_constrain as csctb
import utils_stag_cent_bound_constrain as cscb
import utils_stag_cent_constrain as csc
import utils_prox_J as pJ
import utils_div_constrain as cdiv
import utils_div_bound_constrain as cdivb
import utils_div_tempbound_constrain as cdivtb

def proximalForDynamics(config, boundary):

    if config.dynamics == 0:
        # normal dynamics
        proxCdiv = cdivb.ProxCdivbound(config.M, config.N, config.P,
                                       mx0 = boundary.bx0, mx1 = boundary.bx1
                                       my0 = boundary.by0, my1 = boundary.by1,
                                       f0  = boundary.bt0, f1  = boundary.bt1 )

        proxCsc = cscb.ProxCstagcentbound(config.M, config.N, config.P,
                                          mx0 = boundary.bx0, mx1 = boundary.bx1
                                          my0 = boundary.by0, my1 = boundary.by1,
                                          f0  = boundary.bt0, f1 = boundary.bt1)
        proxJ = pJ.ProxJ(config.gamma)

        proxCb = cb.ProxCbound(config.M, config.N, config.P,
                               mx0 = boundary.bx0, mx1 = boundary.bx1
                               my0 = boundary.by0, my1 = boundary.by1,
                               f0  = boundary.bt0, f1 = boundary.bt1)

    elif config.dynamics == 1:
        # no contrain for m
        proxCdiv = cdivtb.ProxCdivtempbound(config.M, config.N, config.P,
                                            f0 = boundary.bt0, f1 = boundary.bt1)

        proxCsc = csctb.ProxCstagcenttempbound(config.M, config.N, config.P,
                                               f0 = boundary.bt0, f1 = boundary.bt1)
    
        proxJ = pJ.ProxJ(config.gamma)

        proxCb = cb.ProxCtempbound(config.M, config.N, config.P,
                                   f0 = boundary.bt0, f1 = boundary.bt1)

    elif config.dynamics == 2:
        # reservoir
        # for Adr
        proxCdiv = cdiv.ProxCdiv(config.M, config.N, config.P)

        proxCsc = cscrb.ProxCstagcentresbound(config.M, config.N, config.P,
                                              mx0 = boundary.bx0, mx1 = boundary.bx1
                                              my0 = boundary.by0, my1 = boundary.by1,
                                              f0  = boundary.bt0, f1 = boundary.bt1[1:config.M,1:config.N])

        proxJ = pJ.ProxJ(config.gamma)

        proxCb = cb.ProxCresbound(config.M, config.N, config.P,
                                  boundary.deltaM,
                                  mx0 = boundary.bx0, mx1 = boundary.bx1
                                  my0 = boundary.by0, my1 = boundary.by1,
                                  f0  = boundary.bt0, f1 = boundary.bt1[1:config.M,1:config.N])

    elif config.dynamics == 3:
        # reservoir
        # for Adr 3

        proxCdiv = cdiv.ProxCdiv(config.M, config.N, config.P)

        proxCsc = csc.ProxCstagcent(config.M, config.N, config.P)

        proxJ = pJ.ProxJ(config.gamma)

        proxCb = cb.ProxCresbound(config.M, config.N, config.P,
                                  boundary.deltaM,
                                  mx0 = boundary.bx0, mx1 = boundary.bx1
                                  my0 = boundary.by0, my1 = boundary.by1,
                                  f0  = boundary.bt0, f1 = boundary.bt1[1:config.M,1:config.N])

    return proxCdiv,proxCsc,proxJ,proxCb


