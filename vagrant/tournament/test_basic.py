import unittest
from tournament import *


class TestTournament(unittest.TestCase):

    def setUp(self):
        deleteMatches()
        deletePlayers()

    def test_countPlayers(self):
        c = countPlayers()
        self.assertTrue(c == 0, 'countPlayers should return numeric zero')
        print(t)

    def test_registerTestPlayers(self):
        registerPlayer('Steve Jobs')
        pass