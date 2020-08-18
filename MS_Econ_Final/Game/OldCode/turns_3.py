# Play a Game

import mechanics_3 as gm
import pandas as pd

def newGame(dA, dB, hs, r, lp):
    # create decks for players
    deckA = gm.create_deck(dA) 
    deckB = gm.create_deck(dB)  
    # shuffle decks
    gm.shuffleDeck(deckA)
    gm.shuffleDeck(deckB)
    # Player life points 
    playerA = lp
    playerB = lp
    turn = 0
    # starting hand    
    handA = gm.drawCards(hs, deckA, r)
    handB = gm.drawCards(hs, deckB, r)
    fieldA = []
    fieldB = [] 
    grave_A = []
    grave_B = []
    return deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn



def Game(n, dA, dB, lp, hs, r, wa, wb, wc, wx, wy, wz):
    gameplay = pd.DataFrame()
    
    for play in range(n):
        deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn = newGame(dA, dB, hs, r, lp)  
        drawA = [] # cards drawn
        drawB = [] # first 5 for each player
        s_handA = handA
        s_handB = handB
        
        while playerA > 0 and playerB > 0:
            if turn%2 == 0 and deckA != [] and playerA > 0 and playerB > 0:      
                # player A
                handA, turn, draw = gm.DrawPhase(handA, deckA, turn, r)
                drawA = drawA + draw
                handA, fieldA, fieldB, grave_A, grave_B = gm.MainPhase(handA, fieldA, fieldB, grave_A, grave_B, wa, wb, wc)
                
                if turn > 1:
                    fieldA, fieldB, playerB, grave_A, grave_B = gm.BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B, wx, wy, wz)
                else:
                    pass
                
                if playerB <= 0:
                    break

            elif turn%2 != 0 and deckB != [] and playerA > 0 and playerB > 0:
                # player B
                handB, turn, draw = gm.DrawPhase(handB, deckB, turn, r)
                drawB = drawB + draw
                handB, fieldB, fieldA, grave_B, grave_A = gm.MainPhase(handB, fieldB, fieldA, grave_B, grave_A, wa, wb, wc)
                
                if turn > 1:
                    fieldB, fieldA, playerA, grave_B, grave_A = gm.BattlePhase(fieldB, fieldA, playerA, grave_B, grave_A, wx, wy, wz)                    
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
                
        gameplay = gameplay.append({'Turns':turn, 'LP_A':playerA, 'LP_B':playerB,
                                        'MgyA':grave_A.count('monster'),
                                        'MgyB':grave_B.count('monster'),
                                        'SgyA':grave_A.count('spell'), 
                                        'SgyB':grave_B.count('spell'),
                                        'TgyA':grave_A.count('trap'), 
                                        'TgyB':grave_B.count('trap'),
                                        'PrSF':wa[1], 'PrSH':wb[1], 'PrSST':wc[1], 'PrAwMST':wx[1],
                                        'PrAwM':wy[1], 'PrAwST':wz[1], 'HAmr':s_handA.count('monster')/5,
                                        'HAsr':s_handA.count('spell')/5, 'HAtr':s_handA.count('trap')/5,
                                        'HBmr':s_handB.count('monster')/5,'HBsr':s_handB.count('spell')/5,
                                        'HBtr':s_handB.count('trap')/5, 'A5cards':tuple(drawA[0:3]),
                                        'B5cards':tuple(drawB[0:3])},ignore_index=True)
                
    return gameplay


