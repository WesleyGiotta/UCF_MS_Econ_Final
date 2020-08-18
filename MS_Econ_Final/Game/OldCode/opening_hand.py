# Deal 5-card hands at random to player. Write the hands to standard output.
        
# Create a deck 
def create_deck(m, s, t):
    card_types = ['Monster', 'Spell', 'Trap']
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

    