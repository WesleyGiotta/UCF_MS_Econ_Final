# Phases of a turn.

import rules_hand_field as rhf
import random


def DrawPhase(handA, deckA, r=False):
    draw = drawCards(1, deckA, r)
    handA = handA + draw
    return handA, draw
    


def MainPhase(handA, fieldA, fieldB, grave_A, grave_B, wa, wb, wc):
    summon = 0
    if 'monster' in handA and fieldA.count('monster') < 5 and summon == 0:
        handA, fieldA = rhf.Summon(handA, fieldA)
        summon += 1  
        
    if 'spell' in fieldA and ('spell' in fieldB or 'trap' in fieldB):
        # Use spell on field.
        decide_a = random.choices(population=[0,1],weights=wa, k=1)
        if decide_a == [1]:
            fieldA, fieldB, grave_A, grave_B = rhf.Activate_spell_field(fieldA, fieldB, grave_A, grave_B)
        else:
            pass
        
    if 'spell' in handA and fieldA.count('trap') + fieldA.count('spell') < 5:
        if 'trap' in fieldB or 'spell' in fieldB:
            # Use spell from hand.
            decide_b = random.choices(population=[0,1],weights=wb, k=1)
            if decide_b == [1]:
                handA, fieldB, grave_A, grave_B = rhf.Activate_spell_hand(handA, fieldB, grave_A, grave_B)
            else:
                pass
        else:
            pass
        
    if 'trap' in handA or 'spell' in handA:
        if fieldA.count('trap') + fieldA.count('spell') < 5:
            sum_st = handA.count('spell') + handA.count('trap')
            while sum_st > 0:
                sum_st -= 1
                # Set a spell or trap from hand to field.
                handA, fieldA = rhf.set_st(handA, fieldA, wc)
                    
    return handA, fieldA, fieldB, grave_A, grave_B


def BattlePhase(fieldA, fieldB, playerB, grave_A, grave_B, wx, wy, wz):
    if 'monster' in fieldA:
        if 'monster' in fieldB and fieldB.count('trap') + fieldB.count('spell') > 0:
            # opponent has monsters and spells or traps
            decide_x = random.choices(population=[0,1],weights=wx, k=1)
            if decide_x == [1]:
                if 'trap' in fieldB:
                    fieldA, fieldB, grave_A, grave_B = rhf.Activate_trap(fieldA, fieldB, grave_A, grave_B)
                else:
                    fieldA, fieldB, grave_A, grave_B = rhf.Attack(fieldA, fieldB, grave_A, grave_B)
            else:
                pass
            
        elif 'monster' in fieldB and fieldB.count('trap') + fieldB.count('spell') == 0:
            # opponent has monsters and no spell and traps
            decide_y = random.choices(population=[0,1],weights=wy, k=1)
            if decide_y == [1]:
                fieldA, fieldB, grave_A, grave_B = rhf.Attack(fieldA, fieldB, grave_A, grave_B)
            else:
                pass
            
        elif 'monster' in fieldA and 'monster' not in fieldB and fieldB.count('trap') + fieldB.count('spell') > 0:
            # opponent has no monsters but spell or traps
            decide_z = random.choices(population=[0,1],weights=wz, k=1)
            if decide_z == [1]:
                if 'trap' in fieldB:
                    fieldA, fieldB, grave_A, grave_B = rhf.Activate_trap(fieldA, fieldB, grave_A, grave_B)
                else:
                    playerB = rhf.AttackDirect(fieldA, playerB) 
            else:
                pass
            
        elif 'monster' in fieldA and 'monster' not in fieldB and fieldB.count('trap') + fieldB.count('spell') == 0:
            # opponent has no monsters, spell, and traps
            # no need for a decision here bc no risk and all reward
            playerB = rhf.AttackDirect(fieldA, playerB)
    return fieldA, fieldB, playerB, grave_A, grave_B


def EndPhase(playerA, playerB):
    if playerB <= 0:
        return 1
    else:
        return 0


# Create a deck.
def create_deck(d):
    card_types = ['monster', 'spell', 'trap']
    deck = []
    deck += d[0] * [card_types[0]]
    deck += d[1] * [card_types[1]]
    deck += d[2] * [card_types[2]]
    return deck

# Shuffle the deck.
def shuffleDeck(deck):
    import random
    for i in range(len(deck)):
        r = random.randrange(i, len(deck))
        temp = deck[r]
        deck[r] = deck[i]
        deck[i] = temp
        
# Draw top cards from deck.
def drawCards(num, deck, r=False):
    hand = []
    for j in range(num):
        hand += [deck[0]]
        if r == False:
            del deck[0]
        else:
            shuffleDeck(deck)
    return hand






