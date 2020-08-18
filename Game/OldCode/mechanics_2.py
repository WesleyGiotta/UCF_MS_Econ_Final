# version 2.0
# Phases of a turn
def DrawPhase(handA, deckA, turn):
    turn += 1
    handA = handA + drawCards(1, deckA)
    return handA, turn


def MainPhase(handA, fieldA, fieldB, grave_A, grave_B):
    summon = 0
    if 'monster' in handA and fieldA.count('monster') < 5 and summon == 0:
        fieldA.append('monster')
        handA.remove('monster')
        summon += 1        
    if 'trap' in handA and fieldA.count('trap') + fieldA.count('spell') < 5:
        fieldA.append('trap')
        handA.remove('trap')
    if 'spell' in handA and fieldA.count('trap') + fieldA.count('spell') < 5:
        if 'trap' in fieldB:
            handA.remove('spell')
            fieldB.remove('trap')
            grave_A.append('spell')
            grave_B.append('trap')
    return handA, fieldA, fieldB, grave_A, grave_B

  
def BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B):
    if 'monster' in fieldA and 'trap' in fieldB:
        fieldA.remove('monster')
        fieldB.remove('trap')
        grave_A.append('monster')
        grave_B.append('trap')
    elif 'monster' in fieldA and 'monster' in fieldB:
        fieldA.remove('monster')
        fieldB.remove('monster') 
        grave_A.append('monster')
        grave_B.append('monster')
    elif 'monster' in fieldA and 'monster' not in fieldB:
        playerB[1] = playerB[1] - fieldA.count('monster')        
    return fieldA, fieldB, playerB, grave_A, grave_B

            
def EndPhase(playerA, playerB):
    if playerB[1] <= 0:
        return 1
    else:
        return 0


            
# Create a deck 
def create_deck(m, s, t):
    card_types = ['monster', 'spell', 'trap']
    deck = []
    deck += m * [card_types[0]]
    deck += s * [card_types[1]]
    deck += t * [card_types[2]]
    return deck

#deck = create_deck(18, 12, 10)    

# Shuffle the deck.
def shuffleDeck(deck):
    import random
    for i in range(len(deck)):
        r = random.randrange(i, len(deck))
        temp = deck[r]
        deck[r] = deck[i]
        deck[i] = temp

#shuffleDeck(deck)

# draw cards from the shuffled deck without replacement.
def drawCards(num, deck):
    hand = []
    for j in range(num):
        hand += [deck[0]]
        del deck[0]
    return hand

#hand = drawCards(5, deck)
    

# with replacement
def drawCards_r(num, deck):
    hand = []
    for j in range(num):
        hand += [deck[0]]
        shuffleDeck(deck)
    return hand

def DrawPhase_r(handA, deckA, turn):
    turn += 1
    draw = drawCards_r(1, deckA)
    handA = handA + draw
    return handA, turn, draw




