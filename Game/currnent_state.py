# current state and onward simulation

import mechanics_cs as gm
import max_weightFunc_2 as mwf
import pandas as pd
import random

def CurrentState(dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB):
    # create decks for players
    deckA = gm.create_deck(dA) 
    deckB = gm.create_deck(dB)  # make sure to include cards for handB
    # shuffle decks
    gm.shuffleDeck(deckA)
    gm.shuffleDeck(deckB)
    # Player life points 
    playerA = lpA
    playerB = lpB
    turn = t
    # starting hand
    if isinstance(hA, int) == True:   
        handA = gm.drawCards(hA, deckA, r)
    else:
        handA = hA
    handB = gm.drawCards(hsB, deckB, r)
    fieldA = []
    fieldA += fA[0]*['monster'] + fA[1]*['spell'] + fA[2]*['trap']
    fieldB = []
    s = deckB.count('spell')/(deckB.count('spell')+deckB.count('trap'))
    t = 1 - s
    st = random.choices(population=['spell','trap'],weights=[s,t],k=fB[1])
    fieldB += fB[0]*['monster'] + st
    grave_A = []
    grave_B = []
    return deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn



def Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, stratA, stratB, bm_results):
    gameplay = pd.DataFrame()
    
    for play in range(n):
        deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn = CurrentState(dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB)  
        drawA = [] # cards drawn
        drawB=[]
        
        first = random.choice([0,1]) # A = 1 and B = 0
        # strategy given a hand for A
        if stratA == 'ADP':
            sADP, halfA, alwaysA = 1, 0, 0
            x, y, z = mwf.max_weights(first, handA, bm_results)
            wx, wy, wz = [1-x, x], [1-y, y], [1-z, z]
        elif stratA == 'half':
            wx, wy, wz = [0.5,0.5],[0.5,0.5],[0.5,0.5]
            sADP, halfA, alwaysA = 0, 1, 0
                        
        else: # stratA == 'always'
            wx, wy, wz = [0,1],[0,1],[0,1]
            sADP, halfA, alwaysA = 0, 0, 1
        # strategy for B
        if stratB == 'half':
            wx,wy,wz = [0.5,0.5],[0.5,0.5],[0.5,0.5]
            halfB, alwaysB = 1, 0
                        
        else: # stratB == 'always'
            wx, wy, wz = [0,1],[0,1],[0,1]
            halfB, alwaysB = 0, 1
        
        if first == 1:
            firstb = 2 #player A naturally goes first
        else:
            turn += 1# alters the turn count so player B starts
            firstb = 0# change turn back later
        
        while playerA > 0 and playerB > 0:
            if turn%2 == 0 and playerA > 0 and playerB > 0:      
                # player A
                if deckA != []:
                    handA, draw = gm.DrawPhase(handA, deckA, r)
                    drawA = drawA + draw
                else:
                    playerA = playerA - 8
                    break
                                
                turn += 1
                handA, fieldA, fieldB, grave_A, grave_B = gm.MainPhase(handA, fieldA, fieldB, grave_A, grave_B, [0,1], [0,1], [0,1])
                
                # battle phase
                if turn > 1:                        
                    fieldA, fieldB, playerB, grave_A, grave_B = gm.BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B, wx, wy, wz)
                else:
                    pass
                    
                if playerB <= 0:
                    break

            elif turn%2 != 0 and playerA > 0 and playerB > 0:
                # player B
                if deckB != []:
                    handB, draw = gm.DrawPhase(handB, deckB, r)
                    drawB = drawB + draw
                else:
                    playerB = playerB - 8
                    break
                turn += 1
                # main phase
                handB, fieldB, fieldA, grave_B, grave_A = gm.MainPhase(handB, fieldB, fieldA, grave_B, grave_A, [0,1], [0,1], [0,1])
                
                if firstb == 0:
                    turn -= 1 # fixing turn count from B going first
                    firstb += 1
                else:
                    pass

                # battle phase
                if turn > 1:                        
                    fieldB, fieldA, playerA, grave_B, grave_A = gm.BattlePhase(fieldB, fieldA, playerA, grave_B, grave_A, wx, wy, wz)                    
                else:
                    pass
                
                if firstb == 1:
                    turn += 1
                    firstb +=1
                else:
                    pass
                
                if playerA <= 0:
                    break
                
            else:
                break
                
        gameplay = gameplay.append({'LP_A':playerA, 'LP_B':playerB, 'FirstA':first,
                                    'AsADP':sADP, 'AsHalf':halfA, 'AsAlways':alwaysA,
                                    'BsHalf':halfB, 'BsAlways':alwaysB, 
                                    'PrAwMST':wx[1],'PrAwM':wy[1],'PrAwST':wz[1],
                                    'A1_Draw':drawA[0]},ignore_index=True)
                
    return gameplay




