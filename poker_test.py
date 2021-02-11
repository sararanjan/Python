# -*- coding: utf-8 -*-

from random import shuffle
import PokerHand
import unittest 
from pprint import pformat


SORTED_POKER_HANDS = list(["KS AS TS QS JS",
                                          "2H 3H 4H 5H 6H",
                                          "JS JD JC JH 3D",
                                          "AS AD AC AH JD",                                          
                                          "2S AH 2H AS AC",
                                          "2H 3H 5H 6H 7H",
                                          "AS 3S 4S 8S 2S",                                          
                                          "2S 3H 4H 5S 6C",
                                          "2D AC 3H 4H 5S",
                                          "AH AC 5H 6H AS",
                                          "2S 2H 4H 5S 4C",
                                          "AH AC 5H 6H 7S",
                                          "AH AC 4H 6H 7S",
                                          "2S AH 4H 5S KC",
                                          "2S 3H 6H 7S 9C"])

class TestPokerHands (unittest.TestCase)    :

        def test_poker_hands (self):
            lstCopy = SORTED_POKER_HANDS.copy()
            shuffle(lstCopy)    
            print ("The shuffled list:\n", pformat(lstCopy))   
            sorted_list = PokerHand.main(lstCopy)
            sorted_list_hands = [i.split(',',1)[0] for i in sorted_list]
            user_sorted_hands = [i.replace('\'','') for i in sorted_list_hands]
            print ("The sorted list:\n", pformat(user_sorted_hands))            
            user_sorted_hands_iter = iter(user_sorted_hands)
            for hand in SORTED_POKER_HANDS:
                self.assertEqual(next(user_sorted_hands_iter), hand)


if __name__ == '__main__':
    unittest.main()
