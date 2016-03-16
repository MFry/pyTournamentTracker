import unittest
from tournament import *

class TestTournamentDB(unittest.BaseTestSuite):

    def test_countPlayers(self):
        t = countPlayers()
        print(t)