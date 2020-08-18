# for the rough draft
# make sure no color

import random
import pandas as pd

# vectorized version
def PlayerA(weightA, n):
    Player_A = random.choices(population=['Rock','Paper', 'Scissors'],weights=weightA, k=n)
    return Player_A
    
    
def PlayerB(weightB, n):
    Player_B = random.choices(population=['Rock','Paper', 'Scissors'],weights=weightB, k=n)
    return Player_B


def Game(x, wA, wB):
    scoreA = 0
    scoreB = 0
    turns = x
    history = pd.DataFrame() 
    A = PlayerA(wA, x)
    B = PlayerB(wB, x)
    
    for play in range(x):
        if A[play] == B[play]:
            pass
        elif A[play] == 'Rock':
            if B[play] == 'Paper':
                scoreB += 1
            else:
                scoreA += 1    
        elif A[play] == 'Paper':
            if B[play] == 'Scissors':
                scoreB += 1
            else:
                scoreA += 1
        else:
            if B[play] == 'Rock':
                scoreB += 1
            else:
                scoreA += 1
            
    history = history.append({'Turns':turns, 'ScoreA':scoreA, 'ScoreB':scoreB,
                              'wA_Rock':wA[0], 'wA_Paper':wA[1], 'wA_Scissors':wA[2],
                              'wB_Rock':wB[0], 'wB_Paper':wB[1], 'wB_Scissors':wB[2],
                              'weights_A':str(wA), 'weights_B':str(wB)}, ignore_index=True)
                    
    return history

import matplotlib.pyplot as plt

fixed = pd.DataFrame()
for play in range(0,1000):
    fixed = fixed.append(Game(1000, [0.2, 0.6, 0.2], [0.4, 0.5, 0.1]))
# reset the index
fixed = fixed.reset_index()
# delete old index
fixed = fixed.drop(columns=['index'])

# histogram of all the plays
fig = plt.figure()
plt.hist(fixed['ScoreA'], bins=30, color = 'grey')
plt.hist(fixed['ScoreB'], bins=30, color='black', alpha = 0.7)
#plt.show()
fig.savefig('../Figures/hist_1.png')



fixed = pd.DataFrame()
for play in range(0,1000):
    fixed = fixed.append(Game(1000, [1/3, 1/3, 1/3], [1/3, 1/3, 1/3]))
# reset the index
fixed = fixed.reset_index()
# delete old index
fixed = fixed.drop(columns=['index'])

# histogram of all the plays
fig = plt.figure()
plt.hist(fixed['ScoreA'], bins=30, color = 'grey', label="Player A")
plt.hist(fixed['ScoreB'], bins=30, color='black', alpha = 0.7, label="Player B")
plt.xlabel("Total Score from 1000 Rounds")
plt.legend(loc="upper right")
#plt.show()
fig.savefig('../Figures/hist_2.png')



fixed = pd.DataFrame()
for play in range(0,1000):
    fixed = fixed.append(Game(1000, [0.4, 0.5, 0.1], [0.2, 0.6, 0.2]))
# reset the index
fixed = fixed.reset_index()
# delete old index
fixed = fixed.drop(columns=['index'])

# histogram of all the plays
fig = plt.figure()
plt.hist(fixed['ScoreA'], bins=30, color = 'grey')
plt.hist(fixed['ScoreB'], bins=30, color='black', alpha = 0.7)
#plt.show()
fig.savefig('../Figures/hist_3.png')
