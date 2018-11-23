""" DNV-RP-F111 Interference between trawl gear and pipelines """

from math import exp, sqrt

def h_prime(OD, H_sp, L_clump):
    """Return dimensionless height h_prime (DNV-RP-F111 eq. 4.13)"""
    return (H_sp + OD) / L_clump


def Hbar(OD, H_sp, B):
    """Return dimensionless height Hbar (DNV-RP-F111 eq. 4.6)"""
    return (H_sp + OD/2.0 + 0.2) / B


def C_F(OD, B, H_sp=0.0, board='poly'):
    """Return empirical coefficient C_F
    
    ref. DNV-RP-F111:2010 Sec. 4.3 

    Arguments:
    OD -- (float), outside diameter of pipe.
    B -- (float), half height of trawl board. For clump weights: half 
    diameter of roller (D_drum/2).
    H_sp -- (default 0.0), freespan height, ref. F111 Figure 4-1.
    board -- (default 'poly'), trawl board type. 'poly' for polyvalent and 
    rectangular boards (eq. 4.4), 'V-shaped' for V-shaped boards (eq. 4.5).

    
    """
    #if Hbar:
    #    _Hbar = Hbar
    #else:
    #    _Hbar = __import__(__name__).Hbar(OD, H_sp, B)
    _Hbar = Hbar(OD, H_sp, B)
    if board == 'poly':
        return 8.0 * (1. - exp(-0.8*_Hbar))
    elif board == 'V-shaped':
        return 5.8 * (1. - exp(-1.1*_Hbar))
    else:   
        raise ValueError('board not specified correctly in function C_F')   

def k_w(L_w, EA_w=None):
    """Return warp stiffness (DNV-RP-F111 eq. 4.9). 
    
    Arguments:
    L_w -- (float), trawl warp line length.
    EA_w -- (default None) trawl warp line stiffness. If not specified use
    eq. 4.9 (note that the default option requires use of SI units).

    """
    if EA_w:
        return EA_w / L_w
    else:
        return 3.5e7 / L_w


def CW_pullover_force(OD, m_t, L_clump, H_sp=0.0, g=9.81):
    """Return trawl clump weight maximum horizontal pull-over force.
    
    ref. DNV-RP-F111:2010 Sec. 4.4, eq. 4.12 
    
    Arguments:
    OD -- (float), outside diameter of pipe.
    m_t -- (float), clump weight mass.
    L_clump -- (float), distance from reaction point to clump weight COG.
    H_sp -- (default 0.0), freespan height, ref. F111 Figure 4-1.
    g -- (default 9.81), gravitational acceleration.
    
    """
    h_pr = h_prime(OD, H_sp, L_clump)
    return 3.9*m_t*g * (1.0 - exp(-1.8*h_pr)) * (OD/L_clump)**-0.65


def CW_pullover_time(F_p, k_w, V, delta_p=None):
    """Return total clump weight pull-over time.
    
    ref. DNV-RP-F111:2010 Sec. 4.6, eq. 4.23 
    
    Arguments:
    F_p -- (float), see function.
    V -- (float), tow velocity of trawler.
    k_w -- see function k_w in this module.
    delta_p -- (default None), displacement of the pipe at the point of 
    interaction. Normally not set (see note in F111 Sec. 4.4).

        
    """
    if delta_p is None:
        return F_p/(k_w*V) * 1.1
    else:
        return F_p/(k_w*V) + delta_p/V
    

def TB_pullover_force(OD, B, m_t, k_w, V, H_sp=0.0, board='poly'):
    h_pr = h_prime(OD, H_sp, B)
    if board == 'poly':
        _C_F = C_F(OD, B, H_sp=0.0, board='poly')
    else:
        _C_F = C_F(OD, B, H_sp=0.0, board='V-shaped')
    return _C_F*V*sqrt(m_t*k_w)


def TB_pullover_time(m_t, C_F, k_w, C_T=2.0, delta_p=None, V=None):
    """Return total trawl board or beam trawl pull-over time.
    
    ref. DNV-RP-F111:2010 Sec. 4.4, eq. 4.20 
    
    Arguments:
    m_t -- (float), clump weight mass.
    C_F -- see function C_F in this module.
    k_w -- see function k_w in this module.
    C_T -- (default 2.0) coefficient for the pull-over duration (eqs. 4.21 and
    4.22). The default value is applicable for trawl boards.
    delta_p -- (default None), displacement of the pipe at the point of 
    interaction. Normally not set (see note in F111 Sec. 4.4).
    V -- (default None), velocity of the pipe at the point of 
    interaction. Normally not set (see note in F111 Sec. 4.4).
        
    """
    if delta_p is None or V is None:
        return C_T*C_F * sqrt(m_t/k_w) * 1.1
    else:
        return C_T*C_F * sqrt(m_t/k_w) + delta_p/V
    
