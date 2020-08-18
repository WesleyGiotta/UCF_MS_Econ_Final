# rules for the hand and field           
import random   

def select_spell(fieldB, grave_B):
    select = random.choice(['spell', 'trap'])
    if select == 'spell':
        if 'spell' in fieldB:
            fieldB.remove('spell')
            grave_B.append('spell')
        else:
            fieldB.remove('trap')
            grave_B.append('trap')

    else:
        if 'trap' in fieldB:
            fieldB.remove('trap')
            grave_B.append('trap')
        else:
            fieldB.remove('spell')
            grave_B.append('spell')

    return fieldB, grave_B
    
def Activate_spell_hand(handA, fieldB, grave_A, grave_B):
    handA.remove('spell')
    grave_A.append('spell')
    fieldB, grave_B = select_spell(fieldB, grave_B) 
    return handA, fieldB, grave_A, grave_B

def Activate_spell_field(fieldA, fieldB, grave_A, grave_B):
    fieldA.remove('spell')
    grave_A.append('spell')
    fieldB, grave_B = select_spell(fieldB, grave_B)
    return fieldA, fieldB, grave_A, grave_B

def Activate_trap(fieldA, fieldB, grave_A, grave_B):
    fieldA.remove('monster')
    fieldB.remove('trap')
    grave_A.append('monster')
    grave_B.append('trap')
    return fieldA, fieldB, grave_A, grave_B

def Summon(handA, fieldA):
    handA.remove('monster')
    fieldA.append('monster')
    return handA, fieldA

def set_st(handA, fieldA, wc):
    select = random.choices(population=[0,1],weights=wc, k=1)
    if select == [1]:
        st = random.choice(['spell','trap'])
        if st == 'spell':
            if 'spell' in handA:
                handA.remove('spell')
                fieldA.append('spell')
            else:
                handA.remove('trap')
                fieldA.append('trap')
        else:
            if 'trap' in handA:
                handA.remove('trap')
                fieldA.append('trap')
            else:
                handA.remove('spell')
                fieldA.append('spell')
    else:
        pass
    return handA, fieldA

def Attack(fieldA, fieldB, grave_A, grave_B):
    fieldA.remove('monster')
    fieldB.remove('monster')
    grave_A.append('monster')
    grave_B.append('monster')
    return fieldA, fieldB, grave_A, grave_B

def AttackDirect(fieldA, playerB):
    playerB = playerB - fieldA.count('monster')
    return playerB


