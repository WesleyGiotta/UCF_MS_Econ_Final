# Simulate at certain points

import mechanics_cs as gm # used to be mechanics_4
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



def Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, wa, wb, wc, wx, wy, wz):
    gameplay = pd.DataFrame()
    
    for play in range(n):
        deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn = CurrentState(dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB)  
        drawA = [] # cards drawn
        drawB=[]
        s_handA = handA
        
        start = 1 # don't draw on first turn
        
        first = random.choice([0,1]) # A = 1 and B = 0
        if first == 1:
            firstb = 2 #player A naturally goes first
        else:
            turn += 1# alters the turn count so player B starts
            firstb = 0# change turn back later
            
        wxb = wyb = wzb = random.choice([[0,1],[0.5,0.5]])
        
        while playerA > 0 and playerB > 0:
            if turn%2 == 0 and deckA != [] and playerA > 0 and playerB > 0:      
                # player A
                if start != 1:
                    handA, draw = gm.DrawPhase(handA, deckA, r)
                    drawA = drawA + draw
                else:
                    start += 1
                turn += 1
                handA, fieldA, fieldB, grave_A, grave_B = gm.MainPhase(handA, fieldA, fieldB, grave_A, grave_B, wa, wb, wc)
                
                if turn > 1:
                    fieldA, fieldB, playerB, grave_A, grave_B = gm.BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B, wx, wy, wz)
                else:
                    pass
                
                if playerB <= 0:
                    break

            elif turn%2 != 0 and deckB != [] and playerA > 0 and playerB > 0:
                # player B
                if start != 1:
                    handB, draw = gm.DrawPhase(handB, deckB, r)
                    drawB = drawB + draw
                else:
                    start += 1
                turn += 1
                handB, fieldB, fieldA, grave_B, grave_A = gm.MainPhase(handB, fieldB, fieldA, grave_B, grave_A, wa, wb, wc)
                
                if firstb == 0:
                    turn -= 1 # fixing turn count from B going first
                    firstb += 1
                else:
                    pass
               
                if turn > 1:
                    fieldB, fieldA, playerA, grave_B, grave_A = gm.BattlePhase(fieldB, fieldA, playerA, grave_B, grave_A, wxb, wyb, wzb)                    
                else:
                    pass
               
                if firstb == 1:
                    turn += 1
                    firstb +=1
                else:
                    pass
                
                if playerA <= 0:
                    break
                
            elif playerA <= 0 or playerB <= 0:
                break
                
            else:
                if deckA == [] and playerA > 0 and playerB > 0:
                    playerA = playerA - 8
                    # In this format only player A can deck out.
                else: 
                    pass
                
        gameplay = gameplay.append({'LP_A':playerA, 'FirstA':first, 'HAMon':s_handA.count('monster'),
                                    'HASpell':s_handA.count('spell'), 'HATrap':s_handA.count('trap'),
                                    'PrAwMST':wx[1], 'PrAwM':wy[1],'PrAwST':wz[1], 
                                    'Btraps':grave_B.count('trap')},ignore_index=True)
                
    return gameplay


