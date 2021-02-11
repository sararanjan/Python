# -*- coding: utf-8 -*-

#A famous casino is suddenly faced with a sharp decline of their revenues. They decide to offer Texas hold'em also online. Can you help them by writing an algorithm that can rank poker hands?
#
#Task:
#
#Create a poker hand that has a constructor that accepts a string containing 5 cards:
#hand = PokerHand("KS 2H 5C JD TD")
#The characteristics of the string of cards are:
#A space is used as card seperator
#Each card consists of two characters
#The first character is the value of the card, valid characters are:
#`2, 3, 4, 5, 6, 7, 8, 9, T(en), J(ack), Q(ueen), K(ing), A(ce)`
#The second character represents the suit, valid characters are:
#`S(pades), H(earts), D(iamonds), C(lubs)`
#
#The poker hands must be sortable by rank, the highest rank first:
#hands = []
#hands.append(PokerHand("KS 2H 5C JD TD"))
#hands.append(PokerHand("2C 3C AC 4C 5C"))
#hands.sort() (or sorted(hands))
from collections import namedtuple
from random import shuffle
from pprint import pformat

    
class PokerHand(namedtuple('PokerHand', 'face, suit')):    
        def __repr__(self):            
            return ''.join(self)
        
        
suit = 'H D C S'.split()
royal = ['T','J','Q','K','A']
# ordered strings of faces
faces   = '2 3 4 5 6 7 8 9 T J Q K A'
lowaces = 'A 2 3 4 5 6 7 8 9 T J Q K'
# faces as lists
face   = faces.split()
lowace = lowaces.split()
 
handsortorder = {
        "royal-flush": "A",
        "straight-flush": "B",
        "four-of-a-kind":"C",
        "full-house": "D",
         "flush" : "E",
         "straight" : "F",
         "three-of-a-kind": "G",
        "two-pair": "H",
        "one-pair": "I",
        "high-card": "J"        
        }

def royalflush(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if allftypes == set(royal):   
        return 'royal-flush', allfaces
    return False

def straightflush(hand):
    f,fs = ( (lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces) )
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if ( all(card.suit == first.suit for card in rest) and
         ' '.join(card.face for card in ordered) in fs ):        
        return 'straight-flush', ordered[-1].face
    return False
 
def fourofakind(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 4:
            allftypes.remove(f)            
            return 'four-of-a-kind', [f, allftypes.pop()]
    else:
        return False
 
def fullhouse(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)            
            return 'full-house', [f, allftypes.pop()]
    else:
        return False
 
def flush(hand):
    allstypes = {s for f, s in hand}
    if len(allstypes) == 1:
        allfaces = [f for f,s in hand]        
        return 'flush', sorted(allfaces,
                               key=lambda f: face.index(f),
                               reverse=True)
    return False
 
def straight(hand):
    f,fs = ( (lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces) )
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if ' '.join(card.face for card in ordered) in fs:        
        return 'straight', ordered[-1].face
    return False
 
def threeofakind(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if len(allftypes) <= 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)            
            return ('three-of-a-kind', [f] +
                     sorted(allftypes,
                            key=lambda f: face.index(f),
                            reverse=True))
    else:
        return False
 
def twopair(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 2:
        return False
    p0, p1 = pairs
    other = [(allftypes - set(pairs)).pop()]    
    return 'two-pair', pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other
 
def onepair(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 1:
        return False
    allftypes.remove(pairs[0])    
    return 'one-pair', pairs + sorted(allftypes,
                                      key=lambda f: face.index(f),
                                      reverse=True)
 
def highcard(hand):
    allfaces = [f for f,s in hand] 
    return 'high-card', sorted(allfaces,
                               key=lambda f: face.index(f),
                               reverse=True)
 
handrankorder =  (royalflush,straightflush, fourofakind, fullhouse,
                  flush, straight, threeofakind,
                  twopair, onepair, highcard)


def rank(cards):
    hand = handy(cards)
    for ranker in handrankorder:        
        rank = ranker(hand)
        if rank:
            
            break
    assert rank, "Invalid: Failed to rank cards: %r" % cards
    return rank
 
def handy(cards='2H 2D 2C KC QD'):
    hand = []
    for card in cards.split():
        f, s = card[:-1], card[-1]
        assert f in face, "Invalid: Don't understand card face %r" % f
        assert s in suit, "Invalid: Don't understand card suit %r" % s
        hand.append(PokerHand(f,s))
    assert len(hand) == 5, "Invalid: Must be 5 cards in a hand, not %i" % len(hand)
    assert len(set(hand)) == 5, "Invalid: All cards in the hand must be unique %r" % cards
    return hand

def main(hands):
    list_to_sort=[]
    for cards in hands:
        nc = cards
        r = rank(cards)    
        c = handsortorder[r[0]]
        nc = "'"+cards +  "'," +  c
        list_to_sort.append(nc)
        print("%-18r %-15s %r" % (cards, r[0], r[1]))        
        
    #sortedList=BubbleSort.bubbleSort(ListToSort,-1)
    print ("The categorised list:", '\n'.join(list_to_sort))
    list_to_sort.sort(key = lambda list_to_sort: list_to_sort[-1])
    print ("The sorted list inside main:\n",pformat(list_to_sort))        
    return list_to_sort
    

#if __name__ == '__main__': 
#  
#
#    hands1 = list(["KS AS TS QS JS",
#     "2H 3H 4H 5H 6H",
#     "AS AD AC AH JD",
#     "JS JD JC JH 3D",
#     "2S AH 2H AS AC",
#     "AS 3S 4S 8S 2S",     
#     "2H 3H 5H 6H 7H",
#     "2S 3H 4H 5S 6C",
#     "2D AC 3H 4H 5S",
#     "AH AC 5H 6H AS",
#     "2S 2H 4H 5S 4C",
#     "AH AC 5H 6H 7S",
#     "AH AC 4H 6H 7S",
#     "2S AH 4H 5S KC",
#     "2S 3H 6H 7S 9C"     
#     ])
#    lstCopy = hands1.copy()
#    print ("The list:", lstCopy)   
#    shuffle(lstCopy)
#    print ("The shuffled list:", lstCopy)   
#    sorted_list = main(lstCopy)
#    sorted_list_hands = [i.split(',',1)[0] for i in sorted_list]
#    final_list_hands = [i.replace('\'','') for i in sorted_list_hands]
#    print ("The sorted list:\n", pformat(final_list_hands))
        
        