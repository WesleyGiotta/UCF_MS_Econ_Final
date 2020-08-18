# function to output prob winning maximizing weights

def max_weights(first, s_handA, bm_results):
    import pandas as pd
    import numpy as np
    
    m = s_handA.count('monster')
    s = s_handA.count('spell')
    t = s_handA.count('trap')
    
    pA_w = pd.DataFrame()
    for x in [x/10 for x in range(4,9)]:
        for y in [x/10 for x in range(4,9)]:
            for z in [x/10 for x in range(4,9)]:
                v = sum(bm_results.params * [1,first,m,s,t,x,y,z])
                pA_w = pA_w.append({'ProbAwins':np.exp(v)/(1+np.exp(v)),
                                    'Weights':[x,y,z]},ignore_index=True)

    max_w = pA_w.loc[pA_w['ProbAwins'].idxmax()]
    wx, wy, wz = max_w[1][0], max_w[1][1], max_w[1][2]

    return wx, wy, wz


