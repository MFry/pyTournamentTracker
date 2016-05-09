#!/usr/bin/env python
"""
 Test cases for tournament.py
 These tests are not exhaustive, but they should cover the majority of the cases.
"""

import unittest

from tournament import *


class TestTournament(unittest.TestCase):
    def setUp(self):
        delete_matches()
        delete_players()

    def tearDown(self):
        delete_matches()
        delete_players()

    def test_registration_and_count(self):
        """
        Test for initial player count,
                 player count after 1 and 2 players registered,
                 player count after players deleted.
        """
        c = count_players()
        self.assertTrue(c == 0, 'count_players should return numeric zero, but returned {}'.format(c))
        register_player("Chandra Nalaar")
        c = count_players()
        self.assertTrue(c == 1, 'count_players should return 1, but returned {}'.format(c))
        register_player("Jace Beleren")
        c = count_players()
        self.assertTrue(c == 2, 'count_players should return 2, but returned {}'.format(c))
        delete_players()
        c = count_players()
        self.assertTrue(c == 0, 'count_players should return numeric zero, but returned {}'.format(c))

    def test_multi_tournament_registration_count_delete(self):
        """
        Tests counting registered players across multiple tournaments
            player count after 2 players for one tournament, 2 players for another tournament and one player for default tournament
            player count after a tournament is deleted
            player count after the other tournament is deleted
        """
        # TODO: Register current players for additional tournaments
        register_player('awesome person', tournament='t1')
        register_player('terminator', tournament='t1')
        register_player('arnold S')
        register_player('lonely', tournament='t2')
        register_player('not lonely', tournament='t2')
        c = count_registered_players()
        c2 = count_players()
        self.assertFalse(c != 5, 'count_registered_players should return 5 from across 3 tournaments')
        self.assertFalse(c2 != c, 'count_players should return 5 got instead {}'.format(c2))
        delete_tournament(tournament='t1')
        c = count_registered_players()
        c2 = count_players()
        self.assertFalse(c != 3, 'count_registered_players should return 3 from across 2 tournaments')
        self.assertFalse(c2 != 5, 'count_players should return 5 got instead {}'.format(c2))
        delete_tournament(tournament='t2')
        c = count_registered_players()
        c2 = count_players()
        self.assertFalse(c != 1, 'count_registered_players should return 1 from across default tournament')
        self.assertFalse(c2 != 5, 'count_players should return 5 got instead {}'.format(c2))
        p_id = get_player('terminator')
        register_player_to_tournament(p_id)
        p_id = get_player('not lonely')
        register_player_to_tournament(p_id)
        c = count_registered_players()
        self.assertFalse(c != 3,
                         'Two existing players should be registered to the default tournament, got: {}'.format(c))
        c_def = count_registered_players('default')
        self.assertFalse(c != c_def, 'Tournament default should be the only tournament with registered players')
        register_player('Mad Max', 'Crazy Wasteland')
        c_new = count_registered_players('Crazy Wasteland')
        self.assertFalse(c_new > c,
                         '"Crazy Wasteland" should have 1 registered player has {} "default" should have 3 registered players has {}'.format(
                             c_new, c_def))

    def test_get_tournament_and_player_id(self):
        """
         Tests registration and retrieval of tournament id's and player id's
        """
        delete_tournament()

        t_id = get_tournament('default')
        self.assertFalse(t_id, 'No tournament should be returned after deletions.')
        register_tournament('test1')
        t_id = get_tournament('test1')
        self.assertTrue(t_id, 'Tournament was not found')
        register_tournament('test2')
        t_id_test1 = get_tournament('test1')
        t_id_test2 = get_tournament('test2')
        self.assertFalse(t_id_test1 == t_id_test2,
                         "get_tournament is supposed to return two unique id's for 2 tournaments")
        self.assertFalse(t_id_test1 > t_id_test2,
                         'Tournament test1 should return a serial smaller than tournament test2.'
                         'Instead returned test1 : {} test2 : {}'.format(t_id_test1, t_id_test2))
        register_tournament('test3')
        t_id_test3 = get_tournament('test3')
        t_id_test2 = get_tournament('test2')
        t_id_test1 = get_tournament('test1')
        self.assertFalse(t_id_test3 == t_id_test2 or t_id_test2 == t_id_test1 or t_id_test1 == t_id_test3,
                         "get_tournament is supposed to return three unique id's for 3 tournaments")
        self.assertFalse(t_id_test3 < t_id_test2 < t_id_test1,
                         'Tournament test1 should return a serial smaller than tournament test2.'
                         'Instead returned test1 : {} test2 : {}'.format(t_id_test1, t_id_test2, t_id_test3))
        delete_tournament('test3')
        t_id_test = get_tournament('test3')
        self.assertFalse(t_id_test,
                         'Tournament is supposed to be deleted instead "test3" returned {}'.format(t_id_test3))
        delete_tournament()
        t_id_test2 = get_tournament('test2')
        t_id_test1 = get_tournament('test1')
        self.assertFalse(t_id_test2 or t_id_test1, 'Tournaments are not correctly deleted')
        register_tournament('test2')
        t_id_test4 = get_tournament('test2')
        self.assertFalse(t_id_test4 < t_id_test3, 'New tournament "test2" should return a serial larger than'
                                                  'former "test3" id.')
        p_id = get_player('Not Here')
        self.assertFalse(p_id, 'Got an id for a player that does not exist.')
        registered_id = register_player('I M Here')
        p_id = get_player('I M Here')
        self.assertFalse(registered_id != p_id,
                         'Player id does not match ID returned({}) when player was registered({})'.format(p_id,
                                                                                                          registered_id))

    def test_standings_before_matches(self):
        """
        Test to ensure players are properly represented in standings prior
        to any matches being reported.
        """
        register_player("Melpomene Murray")
        register_player("Randy Schwartz")
        standings = player_standings()
        # TODO: Add testing for a 5-tuple return
        self.assertFalse(len(standings) < 2, "Players should appear in player_standings even before "
                                             "they have played any matches.")
        self.assertFalse(len(standings) > 2, "Only registered players should appear in standings.")
        self.assertFalse(len(standings[0]) != 4, "Each player_standings row should have four columns.")
        [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
        self.assertFalse(set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]),
                         "Registered players' names should appear in standings, "
                         "even if they have no matches played.")

    def test_multi_standings_before_match(self):
        """
        Similar test to test_standings_before_matches but with multiple tournaments
        """
        register_player('John Cena', 'wrestling')
        register_player('John Cena', 'wrestling')
        register_player('Bill Gates', 'CE-THROWDOWN')
        register_player('Steve Jobs', 'CE-THROWDOWN')
        standings1 = player_standings('wrestling')
        self.assertFalse(len(standings1) < 2, "Two Players should appear in player_standings even before "
                                              "they have played any matches.")
        standings2 = player_standings('CE-THROWDOWN')
        self.assertFalse(len(standings2) < 2, "Two Players should appear in player_standings even before "
                                              "they have played any matches.")
        self.assertFalse(len(standings1[0]) != 4, "Each player_standings row should have four columns.")
        self.assertFalse(len(standings2[0]) != 4, "Each player_standings row should have four columns.")
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
        register_player("Bruno Walton")
        register_player("Boots O'Neal")
        register_player("Cathy Burton")
        register_player("Diane Grant")
        standings = player_standings()
        [id1, id2, id3, id4] = [row[0] for row in standings]
        report_match({id1: True, id2: False})
        report_match({id3: True, id4: False})
        standings = player_standings()
        for (i, n, w, m) in standings:
            self.assertFalse(m != 1, "Each player should have one match recorded.")
            if i in (id1, id3):
                self.assertFalse(w != 1, "Each match winner should have one win recorded.")
            elif i in (id2, id4):
                self.assertFalse(w != 0, "Each match loser should have zero wins recorded.")
        delete_matches()
        standings = player_standings()
        self.assertFalse(len(standings) != 4, "Match deletion should not change number of players in standings.")
        for (i, n, w, m) in standings:
            if m != 0:
                self.assertFalse(m != 0, "After deleting matches, players should have zero matches recorded.")
                self.assertFalse(w != 0, "After deleting matches, players should have zero wins recorded.")

    def test_swiss_pairing(self):
        """
        Test that pairings are generated properly both before and after match reporting.
        """
        register_player("Twilight Sparkle")
        register_player("Fluttershy")
        register_player("Applejack")
        register_player("Pinkie Pie")
        register_player("Rarity")
        register_player("Rainbow Dash")
        register_player("Princess Celestia")
        register_player("Princess Luna")
        standings = player_standings()
        [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
        pairings = swiss_pairings()
        self.assertFalse(len(pairings) != 4,
                         "P1 Test: For eight players, swiss_pairings should return 4 pairs. Got {pairs}".format(
                             pairs=len(pairings)))
        report_match({id1: True, id2: False})
        report_match({id3: True, id4: False})
        report_match({id5: True, id6: False})
        report_match({id7: True, id8: False})
        pairings = swiss_pairings()
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

    def test_multi_swiss_pairing(self):
        """
            Tests that matches are reported properly before and after reporting for multiple tournaments
            Tests that swiss pairing is properly conducted for multiple tournaments in basic scenarios (no player cross over)

        """
        register_player("George Washington", "Risk")
        register_player("Erwin Rommel", "Risk")
        register_player("Otto von Bismarck", "Risk")
        register_player("Alexander III of Macedon", "Risk")
        register_player("Sun Tzu", "Risk")
        register_player("Napoleon Bonaparte", "Risk")
        register_player("Genghis Khan", "Risk")
        register_player("Hannibal Barca", "Risk")

        register_player("Dollar", "Money")
        register_player("Yen", "Money")
        register_player("Euro", "Money")
        register_player("Yuan", "Money")

        standings1 = player_standings("Risk")
        standings2 = player_standings("Money")
        for standing1 in standings1:
            for standing2 in standings2:
                self.assertFalse(standings1[0] == standings2[0],
                                 'Expected no player crossover. "Risk" tournament, player:{} "Money" tournament, player:{}'.format(
                                     standing1, standing2))

        [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings1]
        report_match({id1: True, id2: False}, "Risk")
        report_match({id3: True, id4: False}, "Risk")
        report_match({id5: True, id6: False}, "Risk")
        report_match({id7: True, id8: False}, "Risk")
        pairings = swiss_pairings("Risk")
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

        [id1, id2, id3, id4] = [row[0] for row in standings2]
        report_match({id1: True, id2: False}, "Money")
        report_match({id3: True, id4: False}, "Money")
        pairings = swiss_pairings("Money")
        [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
        possible_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
        actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
        for pair in actual_pairs:
            if pair not in possible_pairs:
                self.fail('Pair: {} not a possible pair.'.format(str(pair)))


if __name__ == '__main__':
    unittest.main()
