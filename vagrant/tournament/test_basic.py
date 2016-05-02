#!/usr/bin/env python
"""
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
"""
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.
import unittest
from tournament import *


class TestTournament(unittest.TestCase):

    def setUp(self):
        deleteMatches()
        deletePlayers()

    def tearDown(self):
        deleteMatches()
        deletePlayers()

    def test_registration_and_count(self):
        """
        Test for initial player count,
                 player count after 1 and 2 players registered,
                 player count after players deleted.
        """
        c = countPlayers()
        self.assertTrue(c == 0, 'countPlayers should return numeric zero, but returned {}'.format(c))
        registerPlayer("Chandra Nalaar")
        c = countPlayers()
        self.assertTrue(c == 1, 'countPlayers should return 1, but returned {}'.format(c))
        registerPlayer("Jace Beleren")
        c = countPlayers()
        self.assertTrue(c == 2, 'countPlayers should return 2, but returned {}'.format(c))
        deletePlayers()
        c = countPlayers()
        self.assertTrue(c == 0, 'countPlayers should return numeric zero, but returned {}'.format(c))

    def test_multi_tournament_registration_count_delete(self):
        """
        Tests counting registered players across multiple tournaments
        """
        # TODO: Register current players for additional tournaments
        registerPlayer('awesome person', tournament='t1')
        registerPlayer('terminator', tournament='t1')
        registerPlayer('arnold S')
        registerPlayer('lonely', tournament='t2')
        registerPlayer('not lonely', tournament='t2')
        c = countRegisteredPlayers()
        c2 = countPlayers()
        self.assertFalse(c != 5, 'countRegisteredPlayers should return 5 from across 3 tournaments')
        self.assertFalse(c2 != c, 'countPlayers should return 5 got instead {}'.format(c2))
        deleteTournament(tournament='t1')
        c = countRegisteredPlayers()
        c2 = countPlayers()
        self.assertFalse(c != 3, 'countRegisteredPlayers should return 3 from across 2 tournaments')
        self.assertFalse(c2 != 5, 'countPlayers should return 5 got instead {}'.format(c2))
        deleteTournament(tournament='t2')
        c = countRegisteredPlayers()
        c2 = countPlayers()
        self.assertFalse(c != 1, 'countRegisteredPlayers should return 1 from across default tournament')
        self.assertFalse(c2 != 5, 'countPlayers should return 5 got instead {}'.format(c2))

    def test_get_tournament_and_player_id(self):
        """
         Tests registration and retrieval of tournaments
        """
        deleteTournament()
        t_id = getTournament('default')
        self.assertFalse(t_id, 'No tournament should be returned after deletions.')
        registerTournament('test1')
        t_id = getTournament('test1')
        self.assertTrue(t_id, 'Tournament was not found')
        registerTournament('test2')
        t_id_test1 = getTournament('test1')
        t_id_test2 = getTournament('test2')
        self.assertFalse(t_id_test1 == t_id_test2,
                         "getTournament is supposed to return two unique id's for 2 tournaments")
        self.assertFalse(t_id_test1 > t_id_test2,
                         'Tournament test1 should return a serial smaller than tournament test2.'
                         'Instead returned test1 : {} test2 : {}'.format(t_id_test1, t_id_test2))
        registerTournament('test3')
        t_id_test3 = getTournament('test3')
        t_id_test2 = getTournament('test2')
        t_id_test1 = getTournament('test1')
        self.assertFalse(t_id_test3 == t_id_test2 or t_id_test2 == t_id_test1 or t_id_test1 == t_id_test3,
                         "getTournament is supposed to return three unique id's for 3 tournaments")
        self.assertFalse(t_id_test3 < t_id_test2 < t_id_test1,
                         'Tournament test1 should return a serial smaller than tournament test2.'
                         'Instead returned test1 : {} test2 : {}'.format(t_id_test1, t_id_test2, t_id_test3))
        deleteTournament('test3')
        t_id_test = getTournament('test3')
        self.assertFalse(t_id_test,
                         'Tournament is supposed to be deleted instead "test3" returned {}'.format(t_id_test3))
        deleteTournament()
        t_id_test2 = getTournament('test2')
        t_id_test1 = getTournament('test1')
        self.assertFalse(t_id_test2 or t_id_test1, 'Tournaments are not correctly deleted')
        registerTournament('test2')
        t_id_test4 = getTournament('test2')
        self.assertFalse(t_id_test4 < t_id_test3, 'New tournament "test2" should return a serial larger than'
                                                  'former "test3" id.')
        p_id = getPlayer('Not Here')
        self.assertFalse(p_id, 'Got an id for a player that does not exist.')
        registered_id = registerPlayer('I Here')
        p_id = getPlayer('I Here')
        self.assertFalse(registered_id != p_id,
                         'Player id does not match ID returned({}) when player was registered({})'.format(p_id,
                                                                                                          registered_id))

    def test_standings_before_matches(self):
        """
        Test to ensure players are properly represented in standings prior
        to any matches being reported.
        """
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

    def test_multi_standings_before_match(self):
        """
        Similar test to test_standings_before_matches but with multiple tournaments
        """
        registerPlayer('John Cena', 'wrestling')
        registerPlayer('John Cena', 'wrestling')
        registerPlayer('Bill Gates', 'CE-THROWDOWN')
        registerPlayer('Steve Jobs', 'CE-THROWDOWN')
        standings1 = playerStandings('wrestling')
        self.assertFalse(len(standings1) < 2, "Two Players should appear in playerStandings even before "
                                              "they have played any matches.")
        standings2 = playerStandings('CE-THROWDOWN')
        self.assertFalse(len(standings2) < 2, "Two Players should appear in playerStandings even before "
                                              "they have played any matches.")
        self.assertFalse(len(standings1[0]) != 4, "Each playerStandings row should have four columns.")
        self.assertFalse(len(standings2[0]) != 4, "Each playerStandings row should have four columns.")
        [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings1
        self.assertFalse(set([name1, name2]) != set(['John Cena', 'John Cena']),
                         "Registered players' names should appear in standings, "
                         "even if they have no matches played.")
        [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings2
        self.assertFalse(set([name1, name2]) != set(['Bill Gates', 'Steve Jobs']),
                         "Registered players' names should appear in standings, "
                         "even if they have no matches played.")

    def test_report_matches(self):
        """
        Test that matches are reported properly.
        Test to confirm matches are deleted properly.
        """
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

    def test_swiss_pairing(self):
        """
        Test that pairings are generated properly both before and after match reporting.
        """
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
