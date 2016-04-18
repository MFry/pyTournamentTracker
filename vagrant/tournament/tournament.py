#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import networkx as nx


def connect():
    """

    :rtype: psycopg2.connection
    :return:
    """
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament=None):
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    if tournament:
        cur.execute('SELECT id FROM tournaments WHERE name = (%s);', (tournament,))
        tournament_id = cur.fetchone()[0]
        cur.execute('DELETE FROM tournament_players WHERE tournament_id = (%s);', (tournament_id,))
        cur.execute('DELETE FROM matches WHERE t_id = (%s);', (tournament_id,))
    else:
        cur.execute('DELETE FROM tournament_players;')
        cur.execute('DELETE FROM matches;')
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM tournament_players;')
    cur.execute('DELETE FROM players;')
    cur.execute('DELETE FROM matches;')
    conn.commit()
    conn.close()

def countPlayers():
    """
        Returns the number of players currently registered.
    :return:
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT count(*) FROM view_tournament_size;')
    tournaments_player_count = cur.fetchone()
    return int(tournaments_player_count[0])


def registerTournament(tournament):
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO tournaments VALUES (%s) RETURNING id;', (tournament,))
    conn.commit()
    tournament_id = cur.fetchone()[0]
    conn.close()
    return tournament_id


def getTournament(tournament):
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id FROM tournaments WHERE name = %s;', (tournament,))  # TODO: Check the logic on this
    val = cur.fetchone()
    if val:
        tournament_id = val[0]
    else:
        tournament_id = val
    conn.close()
    return tournament_id


def registerPlayer(name, tournament='default'):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).

    :param name:
    :param tournament:
    :return:
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO players VALUES (%s) RETURNING id;', (bleach.clean(name),))
    player_id = cur.fetchone()[0]
    tournament_id = getTournament(tournament)
    if not tournament_id:
        tournament_id = registerTournament(tournament)
    print(player_id, tournament_id)
    cur.execute('INSERT INTO tournament_players VALUES (%s, %s);', (str(player_id), str(tournament_id)))
    conn.commit()
    conn.close()


def playerStandings(tournament='default'):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        t_id: The tournament in which the player's participating in
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # TODO: Figure out if tournament is even necessary
    conn = connect()
    cur = conn.cursor()
    tournament_id = getTournament(tournament)
    if not tournament_id:
        return None
    cur.execute('SELECT player, player_name, games_won, games_played FROM view_player_stats WHERE t_id = %s ORDER BY games_won DESC, games_played DESC;',
                (tournament_id,))
    standings = cur.fetchall()
    conn.close()
    return standings

def reportMatch(players, tournament='default'):
    """
        Records the outcome of a single match between two players/teams.

    :param players: dictionary of
                    key: id numbers of the players
                    value: Boolean whether they won or lost
    :type players: dict of (str, bool)
    :param tournament:
    :return:
    """
    if not tournament:
        raise ValueError('tournament has unsupported value of {}'.format(str(tournament)))
    conn = connect()
    cur = conn.cursor()
    tournament_id = getTournament(tournament)
    cur.execute('SELECT max(match) as last_match FROM matches WHERE t_id = %s;', (tournament_id,))
    last_match = cur.fetchone()[0]
    print(last_match)
    for player in players:
        cur.execute('INSERT INTO matches (t_id, player, winner, match) VALUES (%s, %s, %s, %s);',
                    (tournament_id, player, players[player], last_match+1))
    conn.commit()
    conn.close()


def _generate_players_games_played(matches):
    """
        Based on matches(games played history) this function will return a set containing all the players played and
        a graph representation of who played who (dictionary of key value pairs where the key is the player and value
        is whom they played against).
    :param matches:
    :return:
    :rtype: tuple of set, dict
    """
    players = set()
    for match in matches:
        players.add(match[0])
    plays = {}
    # Initialize games player played against other players
    for player in players:
        plays[player] = set()

    game = 1  # Starting game
    current_game = []

    # create a graph of players who played to create a graph of players who have not played
    for match in matches:
        if game == match[2]:
            current_game.append(match[0])
        else:
            for player in current_game:
                plays[player] = plays[player].union(set(current_game)) - {player}
            game += 1
            current_game = [match[0]]
    return players, plays


def swissPairings(tournament='default'):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    G = nx.Graph()
    standings = playerStandings(tournament)
    # Standings returns: [(1, 'p1', 2, 2), (3, 'p3', 1, 2), (4, 'p4', 1, 2), (2, 'p2', 0, 2)]
    con = connect()
    cur = con.cursor()
    t_id = getTournament(tournament)
    cur.execute('SELECT player, winner, match FROM matches WHERE t_id = (%s);', (t_id,))
    matches = cur.fetchall()
    # returns [(1, True, 1), (2, False, 1), (3, False, 2), (4, True, 2), (1, True, 3), (4, False, 3), (2, False, 4), (3, True, 4)]

    for standing in standings:
        G.add_node(standing[0],
                   name=standing[1],
                   win=standing[2],
                   matches=standing[3])
    # G.nodes() returns [1,2,3....]
    # G.node[1] returns {'name': 'p1', 'matches': 2, 'win': 2}

    players, plays = _generate_players_games_played(matches)

    # plays returns : {1: {2, 4}, 2: {1}, 3: {4}, 4: {1, 3}}
    # Creates an undirected graph of players who have not played against each other
    for player in plays:
        not_played = players - set(plays[player]) - {player}
        # print(not_played) returns {3}, {3,4}, {1,2},{2}
        # print(list(zip([player] * len(not_played), not_played))) returns [(1, 3)], [(2, 3), (2, 4)], [(3, 1), (3, 2)], [(4, 2)]
        weights = list(map(lambda x: abs(G.node[x]['win']+G.node[player]['win']), not_played))
        G.add_weighted_edges_from(list(zip([player] * len(not_played), not_played, weights)))

    res = nx.algorithms.max_weight_matching(G)
    # Convert into tuple pairs
    results = []
    for key in res:
        results.append((key, res[key]))
    return results