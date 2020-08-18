# turns version 2.0
# Two players take turns
import mechanics_2 as gm
import pandas as pd

def newGame():
    # create decks for players
    deckA = gm.create_deck(1, 1, 1) 
    deckB = gm.create_deck(1, 1, 1)  
    # shuffle decks
    gm.shuffleDeck(deckA)
    gm.shuffleDeck(deckB)
    # draw starting hands -> with replacement only
    #handA = gm.drawCards(5, deckA)
    #handB = gm.drawCards(5, deckB)
    # Player life points 
    playerA = ['playerA', 1]
    playerB = ['playerB', 1]
    turn = 0    
    handA = []
    handB = []
    fieldA = []
    fieldB = [] 
    grave_A = []
    grave_B = []
    return deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn

# deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn = newGame()  

# test code 
   
#while playerA[1] > 0 and playerB[1] > 0:
#    if turn%2 == 0:      
#       # player A
#        handA, turn = gm.DrawPhase_r(handA, deckA, turn)
#        print(turn, handA, fieldA, grave_A)
#        handA, fieldA, fieldB, grave_A, grave_B = gm.MainPhase(handA, fieldA, fieldB, grave_A, grave_B)
#        print(turn, handA, fieldA, grave_A)
#        if turn > 1:
#            fieldA, fieldB, playerB, grave_A, grave_B = gm.BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B)
#        print(turn, handA, fieldA, grave_A)    
#        gm.EndPhase(playerA, playerB)
#        
#    else:
#        # player B
#        handB, turn = gm.DrawPhase_r(handB, deckB, turn)
#        print(turn, handB, fieldB, grave_B)
#        handB, fieldB, fieldA, grave_B, grave_A = gm.MainPhase(handB, fieldB, fieldA, grave_B, grave_A)
#        print(turn, handB, fieldB, grave_B) 
#        if turn > 1:
#            fieldB, fieldA, playerA, grave_B, grave_A = gm.BattlePhase(fieldB, fieldA, playerA, grave_B, grave_A)
#        print(turn, handB, fieldB, grave_B)    
#        gm.EndPhase(playerB, playerA)
        

def Game(n):
    gameplay = pd.DataFrame()
    for play in range(n):
        deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn = newGame()  
        drawA = []
        drawB = []
        while playerA[1] > 0 and playerB[1] > 0:
            if turn%2 == 0:      
                # player A
                handA, turn, drawA = gm.DrawPhase_r(handA, deckA, turn)
                handA, fieldA, fieldB, grave_A, grave_B = gm.MainPhase(handA, fieldA, fieldB, grave_A, grave_B)
                if turn > 1:
                    fieldA, fieldB, playerB, grave_A, grave_B = gm.BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B)
                else:
                    pass
                if gm.EndPhase(playerA, playerB):
                    gameplay = gameplay.append({'Turns':turn, 'LP_A':playerA[1], 'LP_B':playerB[1],
                                    'mgyA':grave_A.count('monster'),'mgyB':grave_B.count('monster'),
                                    'sgyA':grave_A.count('spell'), 'sgyB':grave_B.count('spell'),
                                    'tgyA':grave_A.count('trap'), 'tgyB':grave_B.count('trap')},ignore_index=True)
                else:
                    pass
            else:
                # player B
                handB, turn, drawB = gm.DrawPhase_r(handB, deckB, turn)
                handB, fieldB, fieldA, grave_B, grave_A = gm.MainPhase(handB, fieldB, fieldA, grave_B, grave_A)
                if turn > 1:
                    fieldB, fieldA, playerA, grave_B, grave_A = gm.BattlePhase(fieldB, fieldA, playerA, grave_B, grave_A)                    
                else:
                    pass
                if gm.EndPhase(playerB, playerA):
                    gameplay = gameplay.append({'Turns':turn, 'LP_A':playerA[1], 'LP_B':playerB[1],
                                    'mgyA':grave_A.count('monster'),'mgyB':grave_B.count('monster'),
                                    'sgyA':grave_A.count('spell'), 'sgyB':grave_B.count('spell'),
                                    'tgyA':grave_A.count('trap'), 'tgyB':grave_B.count('trap')},ignore_index=True)
                else:
                    pass
                
    return gameplay
        
# test code
# gameplay = Game(1000)



################################################################################################################

# new measurement variables

def Game2(n):
    gameplay = pd.DataFrame()
    
    for play in range(n):
        deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, grave_A, grave_B, turn = newGame()  
        drawA = [] # cards drawn
        drawB = [] # first 5 for each player
        
        while playerA[1] > 0 and playerB[1] > 0:
            if turn%2 == 0:      
                # player A
                handA, turn, draw = gm.DrawPhase_r(handA, deckA, turn)
                drawA = drawA + draw
                handA, fieldA, fieldB, grave_A, grave_B = gm.MainPhase(handA, fieldA, fieldB, grave_A, grave_B)
                
                if turn > 1:
                    fieldA, fieldB, playerB, grave_A, grave_B = gm.BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B)
                else:
                    pass
                if gm.EndPhase(playerA, playerB):
                    gameplay = gameplay.append({'Turns':turn, 'LP_A':playerA[1], 'LP_B':playerB[1],
                                    'mgyA':grave_A.count('monster'),'mgyB':grave_B.count('monster'),
                                    'sgyA':grave_A.count('spell'), 'sgyB':grave_B.count('spell'),
                                    'tgyA':grave_A.count('trap'), 'tgyB':grave_B.count('trap'),
                                    'A5cards':tuple(drawA[0:3]), 'B5cards':tuple(drawB[0:3])},ignore_index=True)
                else:
                    pass
            else:
                # player B
                handB, turn, draw = gm.DrawPhase_r(handB, deckB, turn)
                drawB = drawB + draw
                handB, fieldB, fieldA, grave_B, grave_A = gm.MainPhase(handB, fieldB, fieldA, grave_B, grave_A)
                
                if turn > 1:
                    fieldB, fieldA, playerA, grave_B, grave_A = gm.BattlePhase(fieldB, fieldA, playerA, grave_B, grave_A)                    
                else:
                    pass
                if gm.EndPhase(playerB, playerA):
                    gameplay = gameplay.append({'Turns':turn, 'LP_A':playerA[1], 'LP_B':playerB[1],
                                    'mgyA':grave_A.count('monster'),'mgyB':grave_B.count('monster'),
                                    'sgyA':grave_A.count('spell'), 'sgyB':grave_B.count('spell'),
                                    'tgyA':grave_A.count('trap'), 'tgyB':grave_B.count('trap'),
                                    'A5cards':tuple(drawA[0:3]), 'B5cards':tuple(drawB[0:3])},ignore_index=True)
                else:
                    pass
                
    return gameplay

# gm_test2 = Game2(5)

# add random going first or second
# keep track of the order of play with binary variables
    # make NA if turns not long enough
    # get rid of the vectors of play since too many
# ratios of the starting hand and deck ratios
    

