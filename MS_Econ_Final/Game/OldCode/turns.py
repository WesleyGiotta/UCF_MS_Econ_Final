# Two players take turns
import game_mechanics as gm
  

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
    return deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, turn

deckA, deckB, handA, handB, fieldA, fieldB, playerA, playerB, turn = newGame()  
 
   
while playerA[1] > 0 and playerB[1] > 0:
    if turn%2 == 0:      
        # player A
        handA, turn = gm.DrawPhase_r(handA, deckA, turn)
        print(turn, handA, fieldA)
        handA, fieldA, fieldB = gm.MainPhase(handA, fieldA, fieldB)
        print(turn, handA, fieldA)
        if turn > 1:
            fieldA, fieldB, playerB = gm.BattlePhase(fieldA, fieldB, playerB)
        print(turn, handA, fieldA)    
        gm.EndPhase(playerA, playerB, turn)
        

    else:
        # player B
        handB, turn = gm.DrawPhase_r(handB, deckB, turn)
        print(turn, handB, fieldB)
        handB, fieldB, fieldA = gm.MainPhase(handB, fieldB, fieldA)
        print(turn, handB, fieldB) 
        if turn > 1:
            fieldB, fieldA, playerA = gm.BattlePhase(fieldB, fieldA, playerA)
        print(turn, handB, fieldB)    
        gm.EndPhase(playerB, playerA, turn)
        





