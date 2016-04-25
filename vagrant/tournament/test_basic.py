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


    def test_reportMatches(self):
        registerPlayer("Bruno Walton")
        registerPlayer("Boots O'Neal")
        registerPlayer("Cathy Burton")
        registerPlayer("Diane Grant")
        standings = playerStandings()
        [id1, id2, id3, id4] = [row[0] for row in standings]
        reportMatch({id1: True, id2: False})
        reportMatch({id3: True, id4: False})
        standings = playerStandings()
        for (i, n, w, m) in standings:
            self.assertFalse(m != 1, "Each player should have one match recorded.")
            if i in (id1, id3):
                self.assertFalse(w != 1, "Each match winner should have one win recorded.")
            elif i in (id2, id4):
                self.assertFalse(w != 0, "Each match loser should have zero wins recorded.")
        deleteMatches()
        standings = playerStandings()
        self.assertFalse(len(standings) != 4, "Match deletion should not change number of players in standings.")
        for (i, n, w, m) in standings:
            if m != 0:
                self.assertFalse(m != 0, "After deleting matches, players should have zero matches recorded.")
                self.assertFalse(w != 0, "After deleting matches, players should have zero wins recorded.")

    def test_pairing(self):
        registerPlayer("Twilight Sparkle")
        registerPlayer("Fluttershy")
        registerPlayer("Applejack")
        registerPlayer("Pinkie Pie")
        registerPlayer("Rarity")
        registerPlayer("Rainbow Dash")
        registerPlayer("Princess Celestia")
        registerPlayer("Princess Luna")
        standings = playerStandings()
        [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
        pairings = swissPairings()
        self.assertFalse(len(pairings) != 4, "P1 Test: For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
        reportMatch({id1: True, id2: False})
        reportMatch({id3: True, id4: False})
        reportMatch({id5: True, id6: False})
        reportMatch({id7: True, id8: False})
        pairings = swissPairings()
        [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6),
         (pid7, pname7, pid8, pname8)] = pairings
        possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                              frozenset([id1, id7]), frozenset([id3, id5]),
                              frozenset([id3, id7]), frozenset([id5, id7]),
                              frozenset([id2, id4]), frozenset([id2, id6]),
                              frozenset([id2, id8]), frozenset([id4, id6]),
                              frozenset([id4, id8]), frozenset([id6, id8])
                              ])
        actual_pairs = set(
            [frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
        for pair in actual_pairs:
            if pair not in possible_pairs:
                self.fail('Pair: {} not a possible pair.'.format(str(pair)))


if __name__ == '__main__':
    unittest.main()