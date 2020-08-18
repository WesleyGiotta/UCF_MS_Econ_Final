#Rock-Paper-Scissors

import random
import pandas as pd

def PlayerA(weightA):
    Player_A = random.choices(population=['Rock','Paper', 'Scissors'],weights=weightA, k=1)
    return "".join(Player_A)
    
    
def PlayerB(weightB):
    Player_B = random.choices(population=['Rock','Paper', 'Scissors'],weights=weightB, k=1)
    return "".join(Player_B)


def Game(x, wA, wB):
    scoreA = 0
    scoreB = 0
    turns = 0
    history = pd.DataFrame() 
    
    for play in range(x):
        A = PlayerA(wA)
        B = PlayerB(wB)
        turns += 1
        
        if A == B:
            pass
        elif A == 'Rock':
            if B == 'Paper':
                scoreB += 1
            else:
                scoreA += 1    
        elif A == 'Paper':
            if B == 'Scissors':
                scoreB += 1
            else:
                scoreA += 1
        else:
            if B == 'Rock':
                scoreB += 1
            else:
                scoreA += 1
            
        history = history.append({'Turns':turns, 'ScoreA':scoreA, 'ScoreB':scoreB, 
                                  'A':A, 'B':B, 'weightA':wA,'weightB':wB},ignore_index=True)
                    
    return history


# test
test = Game(100, [1/3, 1/3, 1/3], [1/3, 1/3, 1/3])

# weights for player B fixed
B_fixed = pd.DataFrame()
for y in [x/10 for x in range(0, 11)]:
    for z in [x/10 for x in range(0, 11)]:
        if y + z <= 1 and round(1 - y - z, 1) >= 0:
            B_fixed = B_fixed.append(Game(100, [y, z, round(1-y-z, 1)], [1/3,1/3,1/3]))
        else:
            pass

# both variable -> takes too long maybe vectorized instead?
games = pd.DataFrame()
for a in [x/10 for x in range(0, 11)]:
    for b in [x/10 for x in range(0, 11)]:
        for c in [x/10 for x in range(0, 11)]:
            for d in [x/10 for x in range(0, 11)]:
                if a + b <= 1 and 1 - a - b >= 0 and c + d <=1 and 1 - c - d >= 0:
                    games = games.append(Game(100,[a,b,round(1-a-b,1)],[c,d,round(1-c-d,1)]))
                else:
                    pass

    
    
    