# function to output prob winning maximizing weights

import turns_4 as t4

def max_weights(dA,dB,r,lpA,lpB,hA,hsB,t,fA,fB,games):
    import pandas as pd
#    games = pd.DataFrame()
    # cannot have 100% not attack in infinite deck or else never end
    for z in [x/4 for x in range(0, 4)]:
        # Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, wa, wb, wc, wx, wy, wz)
        games = games.append(t4.Game(10,dA,dB,r,lpA,lpB,hA,hsB,t,fA,fB,
                                     [0,1],[0,1],[0,1],
                                     [0,1], [0,1], [z,1-z]))
    for y in [x/4 for x in range(0, 4)]:
        # Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, wa, wb, wc, wx, wy, wz)
        games = games.append(t4.Game(10,dA,dB,r,lpA,lpB,hA,hsB,t,fA,fB,
                                     [0,1],[0,1],[0,1],
                                     [0,1], [y,1-y], [0,1]))
    for x in [x/4 for x in range(0, 4)]:
        # Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, wa, wb, wc, wx, wy, wz)
        games = games.append(t4.Game(10,dA,dB,r,lpA,lpB,hA,hsB,t,fA,fB,
                                     [0,1],[0,1],[0,1],
                                     [x,1-x], [0,1], [0,1]))

    # change non-ones to zeros if not zero
    # sometimes loss can have negatives
    # a negative can show that you are lossing worse though
    games.loc[games.LP_A <= 0, "LP_A"] = 0
    # make winning binomial
    games.loc[games.LP_A >= 1, "LP_A"] = 1
    
    # train-test split
    from sklearn.model_selection import train_test_split

    train_data, test_data = train_test_split(games,
                                             test_size = 0.20,
                                             random_state = 42)

    # GLM binomial family

    from patsy import dmatrices
    import numpy as np

    formula = ('LP_A ~ PrAwMST + PrAwM + PrAwST')

    #Carve out the training matrices from the training data frame using the regression formula
    y_train, X_train = dmatrices(formula, train_data, return_type='dataframe')
    #Carve out the testing matrices from the testing data frame using the regression formula
    y_test, X_test = dmatrices(formula, test_data, return_type='dataframe')
        
    if y_train['LP_A'].sum() == 0 or y_train['LP_A'].sum() == len(y_train['LP_A']):
        wx, wy, wz = 1,1,1
        
    else:
        import statsmodels.api as sm
        binom_model = sm.GLM(y_train, X_train, family=sm.families.Binomial())
        bm_results = binom_model.fit()

        pA_w = pd.DataFrame()
        for x in [x/10 for x in range(4,11)]:
            for y in [x/10 for x in range(4,11)]:
                for z in [x/10 for x in range(4,11)]:
                    v = sum(bm_results.params * [1,x,y,z])
                    pA_w = pA_w.append({'ProbAwins':np.exp(v)/(1+np.exp(v)),
                                        'Weights':[x,y,z]},ignore_index=True)

        max_w = pA_w.loc[pA_w['ProbAwins'].idxmax()]
        wx, wy, wz = max_w[1][0], max_w[1][1], max_w[1][2]

    return wx, wy, wz

