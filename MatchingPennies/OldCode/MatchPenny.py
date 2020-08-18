# Matching Pennies Simulator
# Player should converge to mixed strategy 0.5 head and 0.5 tails.
# Rules
# both player pick H or T 
# if match Player A wins, if not Player B wins



import random
import pandas as pd

def PlayerA(weightA, r):
    random.seed(r)
    Player_A = random.choices(population=['H','T'],weights=weightA, k=1)
    return "".join(Player_A)

# the random seed is not working
def PlayerB(weightB, r):
    random.seed(r)
    Player_B = random.choices(population=['H','T'],weights=weightB, k=1)
    return "".join(Player_B)


def weight_adjust(scoreA, scoreB, wA, wB, history, start, stop):
    if (history.iloc[stop-1,2] - history.iloc[start,2]) - (history.iloc[stop-1,3] - history.iloc[start,3]) >= 4:
        if history.iloc[start:stop,0].eq('H').astype(int).sum() > history.iloc[start:stop,0].eq('T').astype(int).sum():
            wB[0] = wB[0] - 0.05
            wB[1] = wB[1] + 0.05
        else:
            wB[0] = wB[0] + 0.05
            wB[1] = wB[1] - 0.05
    elif (history.iloc[stop-1,2] - history.iloc[start,2]) - (history.iloc[stop-1,3] - history.iloc[start,3]) <= -4:
        if history.iloc[start:stop,1].eq('H').astype(int).sum() > history.iloc[start:stop,1].eq('T').astype(int).sum():
            wA[0] = wA[0] + 0.05
            wA[1] = wA[1] - 0.05
        else:
            wA[0] = wA[0] - 0.05
            wA[1] = wA[1] + 0.05
    else:
        pass
    start += 20
    stop += 20 
    return wA, wB, start, stop


def Game(x):
    scoreA = 0
    scoreB = 0
    turns = 0
    wA = [0.0, 1.0]
    wB = [1.0, 0.0]
    start = 0
    stop = 20
    rA = 1
    rB = 0
    history = pd.DataFrame() 
    
    for play in range(x):
        A = PlayerA(wA, rA)
        B = PlayerB(wB, rB)
        
        while turns%20 == 0 and turns != 0:
            wA, wB, start, stop = weight_adjust(scoreA, scoreB, wA, wB, history, start, stop) 
            break
    
        if A == B:
            scoreA += 1
        else: 
            scoreB += 1

        turns += 1
        rA += 2
        rB += 2
        history = history.append({'Turns':turns, 'ScoreA':scoreA, 'ScoreB':scoreB,
                                  'WeightA_heads':wA[0], 'WeightB_heads':wB[0],
                                  'A':A, 'B':B}, ignore_index=True)
                    
    return history

game_mp = Game(6000)

# I need to set I margin of error for the when to change weights 
# or else it will always want to change i.e. never settle at 0.5

# ...
# still not really settling


import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12,4))

plt.scatter(game_mp["Turns"], game_mp["WeightA_heads"], color="blue", label="PlayerA")
plt.scatter(game_mp["Turns"], game_mp["WeightB_heads"], color="red", label="PlayerB")
plt.axhline(y=0.5, color="green", linestyle="-")
plt.ylabel("Probability of Picking Heads")
plt.xlabel("Number of Turns")
plt.legend(loc="lower right")

plt.show()

fig.savefig('./Desktop/Yugioh_final/Presentation_7_3/Pictures/scatter_1.png')


# saving dataframe to csv
game_mp.head(10).to_csv('./Desktop/Yugioh_final/Appendix/csv/head_mp.csv', encoding='utf-8', index=False)



