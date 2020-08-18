# Rock Paper Scissors Vectorized

import random
import pandas as pd

# testing vectorization of player
#def Player(weightA,n):
#    Player = random.choices(population=['Rock','Paper', 'Scissors'],weights=weightA, k=n)
#    return Player
#
#player10 = Player([0.1,0.4,0.5],10)
#player10[0]

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

# test function
test = Game(100, [1/3, 1/3, 1/3], [1/3, 1/3, 1/3])


# weight B is fixed
B_fixed = pd.DataFrame()
for y in [x/10 for x in range(0, 11)]:
    for z in [x/10 for x in range(0, 11)]:
        if y + z <= 1 and round(1 - y - z, 1) >= 0:
            B_fixed = B_fixed.append(Game(1000, [y, z, round(1-y-z, 1)], [1/3,1/3,1/3]))
        else:
            pass
# reset the index
B_fixed = B_fixed.reset_index()
# delete old index
B_fixed = B_fixed.drop(columns=['index'])


# both variable
games = pd.DataFrame()
for a in [x/10 for x in range(0, 11)]:
    for b in [x/10 for x in range(0, 11)]:
        for c in [x/10 for x in range(0, 11)]:
            for d in [x/10 for x in range(0, 11)]:
                if a + b <= 1 and 1 - a - b >= 0 and c + d <=1 and 1 - c - d >= 0:
                    games = games.append(Game(1000,[a,b,round(1-a-b,1)],[c,d,round(1-c-d,1)]))
                else:
                    pass

# append the nash equilibrium
games = games.append(Game(1000,[1/3, 1/3, 1/3],[1/3, 1/3, 1/3]))
# create a new index
games = games.reset_index()
# delete old index
games = games.drop(columns=['index'])




import matplotlib.pyplot as plt

fig = plt.figure()

plt.scatter(B_fixed["weights_A"],B_fixed["ScoreA"]/100, color="blue", alpha=0.5)
plt.scatter(B_fixed["weights_A"],B_fixed["ScoreB"]/100, color="red", alpha=0.5)
plt.show()

fig.savefig('./Desktop/test.png')

B_fixed.groupby('wA_Rock', as_index=False)['ScoreA'].mean()

# row with the max values
max_A = B_fixed[B_fixed['ScoreA'] == B_fixed['ScoreA'].max()]
max_B = B_fixed[B_fixed['ScoreB'] == B_fixed['ScoreB'].max()]



group = games.groupby('weights_A', as_index=False)['ScoreA'].mean()




plt.hist(games['ScoreA'], bins = 64)
plt.show()


# didnt help
plt.scatter(games['wA_Rock'],games['ScoreA']/100, color="blue", alpha=0.5)
plt.scatter(games['wB_Rock'],games['ScoreB']/100, color="red", alpha=0.5)
plt.show()

