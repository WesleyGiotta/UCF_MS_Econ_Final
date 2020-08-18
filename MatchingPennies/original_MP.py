# Matching Pennies
import random
import pandas as pd

def PlayerA(weightA):
    Player_A = random.choices(population=['H','T'],weights=weightA, k=1)
    return "".join(Player_A)

def PlayerB(weightB):
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
    history = pd.DataFrame() 
    
    for play in range(x):
        A = PlayerA(wA)
        B = PlayerB(wB)
        
        while turns%20 == 0 and turns != 0:
            wA, wB, start, stop = weight_adjust(scoreA, scoreB, wA, wB, history, start, stop) 
            break
    
        if A == B:
            scoreA += 1
        else: 
            scoreB += 1

        turns += 1

        history = history.append({'Turns':turns, 'ScoreA':scoreA, 'ScoreB':scoreB,
                                  'WeightA_heads':wA[0], 'WeightB_heads':wB[0],
                                  'A':A, 'B':B}, ignore_index=True)
                    
    return history



