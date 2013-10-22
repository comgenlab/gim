import math

def calc(l1,l2,p):
    """RBO indefinite rank similarity metric.

    As described in:
    Webber, W., Moffat, A., & Zobel, J. (2010). 
    A similarity measure for indefinite rankings. 
    ACM Transactions on Information Systems.
    doi:10.1145/1852102.1852106.

    The RBO formula was modified to handle ties (items at same rank)
    as explained by Dr. William Webber on: 
    http://blog.codalism.com/?p=1317

    USAGE:
    >>> l1 = {1:['A'],2:['B','C'],3:['D']}
    >>> l2 = {1:['A'],2:['B','C'],3:['D']}
    >>> print rbo(l1,l2,0.98)
    1.0
    """

    l1l = len(l1)
    l2l = len(l2)
    l = [(l1l, l1),(l2l,l2)]
    if l1l <= l2l:
       sl, ll = l
    else:
       ll, sl = l
    # si/li - length (no. of ranks) of short/long list.
    # S/L   - short/long list.
    si, S = sl
    li, L = ll

    # Calculate Agreements (A) at ranks d=1 through li.
    ss = set([])
    ls = set([])
    A = {}
    for d in L:
        # i - item at rank d.
        for i in L[d]:
            ls.add(i)
        # Check if short list still goes.
        if d <= si:
            for i in S[d]:
                ss.add(i)
        # X_d - no. of intersected items at rank d.     
        X_d = len(ss.intersection(ls))
        # X_s/X_l - no. of itersected items of short/long list.
        # s/l - no. of all items of short/long list.
        if d == si:
            X_s = X_d
            s = float(len(ss))
        if d == li:
            X_l = X_d
            l = float(len(ls)) 
        # A_d - Agreement at rank d.
        A_d = 2.0*X_d/(len(ss) + len(ls)) if (ss and ls) else 0.0
        A[d] = A_d
   
    # Part 1: \sum_{d=1}^{l}A_d*p^d
    p1 = 0
    for d in L:
        p1+=A[d]*pow(p,d)

    # Part 2: \sum_{d=s+1}^{l}A_s\frac{(d-s)}{d}p^d
    p2 = 0
    for d in range(si+1,li+1):
        p2+=A[si]*(d-float(si))/d*pow(p, d)

    # Part 3: \frac{X_l-X_s}{s}+A_s\right)p^li
    p3 = ((X_l - X_s)/l + A[si])*pow(p, li) 

    # Final Equation. 
    rbo_ext = (1-p)/p*(p1+p2)+p3
    return rbo_ext
   


def weight(d,p):
    '''
    Returns the weight of the prefix of length d (1:d).

    USAGE:
    >>> weight(10,0.9)
    0.86
    It means that for p=0.9 first 10 ranks have 86% 
    of the weight of the evaluation.

    >>> weight(50,0.98)
    0.86
    It means that to give the top 50 ranks the same weight
    one should use p=0.98.
    '''

    # Part 1: 
    p1 = 1-pow(p,d-1)
    # Part 2
    p2 = ((1-p)/p)*d
    # Part 3: 
    p3 = math.log(1.0/(1-p))
    # Part 4:
    p4 = 0
    for i in range(1,d):
       p4+=pow(p,i)/float(i)

    # Final Equation.
    wrbo = p1 + p2 * (p3-p4)
    return wrbo



if __name__ == "__main__":
    # Test pair: gives 0.72 as shown on http://blog.codalism.com/?p=1317
    l1a = {1:['A'],2:['B'],3:['C'],4:['D'],5:['E'],6:['H']} 
    l1b = {1:['D'],2:['B'],3:['F'],4:['A']}
    print(rbo(l1a,l1b,0.98))


    # Test pair: gives 1
    l2a = {1: ['A','B','C'], 2:['D'], 3:['E']}
    l2b = {1: ['A','B','C'], 2:['D'], 3:['E']}
    print(rbo(l2a,l2b,0.98))


    # Test pair:
    l3a = {1: ['A','B','C'], 2:['D'], 3:['W'], 4:['H'], 5:['E']}
    l3b = {1: ['A','B','C'], 2:['D'], 3:['E']}
    print(rbo(l3a,l3b,0.98))

    # Test pair:
    l3a = {1: ['A','B','C'], 2:['D'], 3:['E'], 4:['H'],5:['W'],6:['T','U'],
           7:['O','P'],8:['R','S'],9:['W','X']}
    l3b = {1: ['A','B','C'], 2:[], 3:[], 4:['U']}
    print(rbo(l3a,l3b,0.98))
