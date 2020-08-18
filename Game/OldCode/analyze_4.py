# Example Game

import turns_4 as t4
import pandas as pd

# Deck size [monster, spell, trap].
dA=[1,1,1]
dB=[1,1,1]

hA = ['monster']
fA = [0,0,0]
fB = [0,1]

# weights for using/setting spell
# Use spell on field.
wa=[0,1]
# Use spell from hand.
wb=[0,1]
# Set a spell or trap from hand to field.
wc=[0,1]

# weights for attacking
# opponent has monsters and spells or traps
wx=[0,1]
# opponent has monsters and no spell and traps
wy=[0,1]
# opponent has no monsters but spell or traps
wz=[0,1]


# data
# Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, wa, wb, wc, wx, wy, wz)
gameplay = t4.Game(100,dA,dB,True,1,1,hA,0,2,fA,fB,wa, wb, wc, wx, wy, wz)

games = pd.DataFrame()
for y in [x/5 for x in range(0, 5)]:
    for z in [x/5 for x in range(0, 5)]:
        games = games.append(t4.Game(100,dA,dB,True,1,1,hA,0,2,fA,fB,
                                     [0,1],[0,1],[0,1],
                                     [0,1], [y,1-y], [z,1-z]))
for x in [x/5 for x in range(0, 5)]:
    for y in [x/5 for x in range(0, 5)]:
        games = games.append(t4.Game(100,dA,dB,True,1,1,hA,0,2,fA,fB,
                                     [0,1],[0,1],[0,1],
                                     [x,1-x], [y,1-y], [0,1]))
for x in [x/5 for x in range(0, 5)]:
    for z in [x/5 for x in range(0, 5)]:
        games = games.append(t4.Game(100,dA,dB,True,1,1,hA,0,2,fA,fB,
                                     [0,1],[0,1],[0,1],
                                     [x,1-x], [0,1], [z,1-z]))        

games = pd.DataFrame()
# cannot have 100% not attack in infinite deck or else never end
for x in [x/10 for x in range(0, 7)]:
    for y in [x/10 for x in range(0, 7)]:
        for z in [x/10 for x in range(0, 7)]:
            games = games.append(t4.Game(100,dA,dB,True,1,1,hA,0,1,fA,fB,
                                         [0,1],[0,1],[0,1],
                                         [x,1-x], [y,1-y], [z,1-z]))

#games.reset_index()

# fequency of wins and losses
games["LP_A"].value_counts()

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

import statsmodels.api as sm
from patsy import dmatrices

formula = ('LP_A ~ PrAwMST + PrAwM + PrAwST')

#Carve out the training matrices from the training data frame using the regression formula
y_train, X_train = dmatrices(formula, train_data, return_type='dataframe')
#Carve out the testing matrices from the testing data frame using the regression formula
y_test, X_test = dmatrices(formula, test_data, return_type='dataframe')


binom_model = sm.GLM(y_train, X_train, family=sm.families.Binomial())
bm_results = binom_model.fit()
bm_results.summary()


# prob of winning
import numpy as np
# v = sum(bm_results.params * [1,0.5,0.5,0.5])
# odds = np.exp(bm_results.params)
# prob = odds / (1+odds)

# prob A wins
# v = b_0 + b_1 * x_1 + ... + b_n * x_n
# A_w = np.exp(v)/(1+np.exp(v))

pA_w = pd.DataFrame()
for x in [x/10 for x in range(0, 11)]:
    for y in [x/10 for x in range(0, 11)]:
        for z in [x/10 for x in range(0, 11)]:
            v = sum(bm_results.params * [1,x,y,z])
            pA_w = pA_w.append({'ProbAwins':np.exp(v)/(1+np.exp(v)),
                                'Weights':[x,y,z]},ignore_index=True)

max_w = pA_w.loc[pA_w['ProbAwins'].idxmax()]


