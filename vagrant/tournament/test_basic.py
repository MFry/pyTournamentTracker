import unittest
from tournament import *


class TestTournament(unittest.TestCase):

    def setUp(self):
        deleteMatches()
        deletePlayers()

    def tearDown(self):
        deleteMatches()
        deletePlayers()

    def test_count(self):
        c = countPlayers()
        self.assertTrue(c == 0, 'countPlayers should return numeric zero')
        registerPlayer("Chandra Nalaar")
        c = countPlayers()
        self.assertTrue(c == 1, 'countPlayers should return 1, but returned {}'.format(c))
        registerPlayer("Jace Beleren")
        c = countPlayers()
        self.assertTrue(c == 2, 'countPlayers should return 2, but returned {}'.format(c))
        deletePlayers()
        c = countPlayers()
        self.assertTrue(c == 0, 'countPlayers should return numeric zero, but returned {}'.format(c))

    def testStandingsBeforeMatches(self):
        registerPlayer("Melpomene Murray")
        registerPlayer("Randy Schwartz")
        standings = playerStandings()
        # TODO: Add testing for a 5-tuple return
        self.assertFalse(len(standings) < 2, "Players should appear in playerStandings even before "
                         "they have played any matches.")
        self.assertFalse(len(standings) > 2, "Only registered players should appear in standings.")
        self.assertFalse(len(standings[0]) != 4, "Each playerStandings row should have four columns.")
        [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
        self.assertFalse(set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]), "Registered players' names should appear in standings, "
                         "even if they have no matches played.")


    def test_registerTestPlayers(self):
        registerPlayer('Steve Jobs')
        pass


if __name__ == '__main__':
    unittest.main()