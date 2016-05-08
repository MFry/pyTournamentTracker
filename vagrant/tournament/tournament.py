#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import networkx as nx


def connect():
    """
        Establishes a connection to the tournament database

    :rtype: psycopg2.connection
    :return: psycop2g connection object to the tournament database
    """
    return psycopg2.connect("dbname=tournament")


def delete_matches(tournament=None):
    """
        Removes all the match records from the database unless a tournament is chosen then it
        removes match history specifically from that tournament.

        :param tournament: Name of the tournament from which to delete the matches
            :type tournament: str
    """
    conn = connect()
    cur = conn.cursor()
    if tournament:
        cur.execute('SELECT id FROM tournaments WHERE name = (%s);', (tournament,))
        tournament_id = cur.fetchone()[0]
        cur.execute('DELETE FROM matches WHERE t_id = (%s);', (tournament_id,))
    else:
        cur.execute('DELETE FROM matches;')
    conn.commit()
    conn.close()


def delete_players():
    """
        Remove all the players. NOTE: This will remove the player tournament registration as well as their match records from the database.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM tournament_players;')
    cur.execute('DELETE FROM players;')
    cur.execute('DELETE FROM matches;')
    conn.commit()
    conn.close()


def delete_tournament(tournament=None):
    """
        Removes all tournaments unless a tournament is given. NOTE: This will remove all the player registrations (not players) and any matches associated with the tournament.
        If tournament is not found an exception is raised

    :param tournament: Name of the tournament to be deleted.
        :type tournament: str
    """
    conn = connect()
    cur = conn.cursor()

    if tournament:
        t_id = getTournament(tournament)
        if not t_id:
            raise psycopg2.ProgrammingError('{} not found in tournaments table'.format(tournament))
        cur.execute('DELETE FROM tournament_players WHERE tournament_id = %s;', (t_id,))
        cur.execute('DELETE FROM matches WHERE tournament_id = %s;', (t_id,))
        cur.execute('''DELETE FROM tournaments WHERE ctid IN (
                       SELECT ctid
                        FROM tournaments
                        WHERE id = %s
                        LIMIT 1
                    );''', (t_id,))
        # http://stackoverflow.com/questions/5170546/how-do-i-delete-a-fixed-number-of-rows-with-sorting-in-postgresql
    else:
        cur.execute('DELETE FROM tournament_players;')
        cur.execute('DELETE FROM matches;')
        cur.execute('DELETE FROM tournaments;')
    conn.commit()
    conn.close()


def countPlayers():
    """

    :return: Returns the total number of players currently registered
        :rtype: int
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT count(*) FROM players;')
    player_count = cur.fetchone()
    conn.close()
    if not player_count[0]:
        return 0
    return int(player_count[0])


def countRegisteredPlayers():
    """

    :return: Returns the number of players currently registered in tournaments.
        :rtype: int
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT sum(total_players) FROM view_tournament_size;')
    tournaments_player_count = cur.fetchone()
    if not tournaments_player_count[0]:
        return 0
    return int(tournaments_player_count[0])
    conn.close()


def registerTournament(tournament):
    """
        Registers a new tournament. Note the tournament name has to be unique otherwise an exception
            (psycopg2.DatabaseError) is raised

    :param tournament: The name of the new tournament to be registered
        :type tournament: str
    :return: Returns the unique assigned id of the new tournament
        :rtype: int
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO tournaments VALUES (%s) RETURNING id;', (tournament,))
    conn.commit()
    tournament_id = cur.fetchone()[0]
    conn.close()
    return tournament_id


def registerPlayer(name, tournament='default'):
    """
    Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    :param name: the player's full name (need not be unique).
        :type name: str
    :param tournament: The name of the tournament the player will participate in
        :type tournament: str
    :return: Returns the unique assigned id of the new player
        :rtype: int
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO players VALUES (%s) RETURNING id;', (bleach.clean(name),))
    player_id = cur.fetchone()[0]
    tournament_id = getTournament(tournament)
    # Check if tournament exists
    if not tournament_id:
        tournament_id = registerTournament(tournament)
    # link player to tournament
    cur.execute('INSERT INTO tournament_players VALUES (%s, %s);', (str(player_id), str(tournament_id)))
    conn.commit()
    conn.close()
    return player_id


def register_player_to_tournament(player_id, tournament='default'):
    pass


def getTournament(tournament):
    """
        Finds the tournament id for a given tournament name

    :param tournament: The name of the tournament
        :type tournament: str
    :return: An id of the tournament
        :rtype: int
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id FROM tournaments WHERE name = %s LIMIT 1;', (tournament,))
    val = cur.fetchone()
    if val:
        tournament_id = val[0]
    else:
        tournament_id = val
    conn.close()
    return tournament_id


def getPlayer(player):
    """
        Finds the unique id of the first registered player with the name

    :param player: Name of the player to be found
        :type player: str
    :return: First result of a player with the given name
        :rtype int
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id FROM players WHERE name = %s LIMIT 1;', (player,))
    val = cur.fetchone()
    if val:
        player_id = val[0]
    else:
        player_id = val
    conn.close()
    return player_id


def playerStandings(tournament='default'):
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.


    :param tournament: Name of the tournament from which to return the standings of the players
        :type tournament: str
    :return:
          A list of tuples, each of which contains (id, name, wins, matches):
            p_id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played

    """
    conn = connect()
    cur = conn.cursor()
    tournament_id = getTournament(tournament)
    if not tournament_id:
        return None
    cur.execute(
        'SELECT p_id, player_name, games_won, games_played FROM view_player_stats WHERE t_id = %s ORDER BY games_won DESC, games_played DESC;',
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
        :type tournament: str
    """
    if not tournament:
        raise ValueError('tournament has unsupported value of {}'.format(str(tournament)))
    conn = connect()
    cur = conn.cursor()
    tournament_id = getTournament(tournament)
    cur.execute('SELECT COALESCE(max(match),0) as last_match FROM matches WHERE tournament_id = %s;', (tournament_id,))
    last_match = cur.fetchone()[0]
    last_match += 1
    # print(last_match)
    for player in players:
        cur.execute('INSERT INTO matches (tournament_id, player, winner, match) VALUES (%s, %s, %s, %s);',
                    (tournament_id, player, players[player], last_match))
    conn.commit()
    conn.close()


def _generate_players_games_played(standings, matches):
    """
        Based on matches(games played history) this function will return a set containing all the players played and
        a graph representation of who played who (dictionary of key value pairs where the key is the player and value
        is whom they played against).
    :param matches:
    :return:
        Sample return:
            players : {1,2,3, ...}
            plays returns : {1: {2, 4}, 2: {1}, ...}
    :rtype: tuple of set, dict
    """
    players = set()
    plays = {}
    # Initialize games player played against other players
    for player_stats in standings:
        players.add(player_stats[0])
        plays[player_stats[0]] = set()

    game = 1  # Starting game
    current_game = []

    # create a graph of players who played to create a graph of players who have not played
    # create a graph of players who played to create a graph of players who have not played
    for match in matches:
        match = [int(i) for i in match[0].split( ',')]
        match = set(match)
        for player in match:
            plays[player] = plays[player].union(set(match)) - {player}
    return players, plays


def _generate_match_history(tournament):
    """

    :param tournament:
    :return:
        Sample return: [('2,5',..), ('4,6',), ('1,3',)] where
            where each tuple returns everyone that played during the specific match
    """
    conn = connect()
    cur = conn.cursor()
    t_id = getTournament(tournament)
    cur.execute('''SELECT array_to_string(array_agg(DISTINCT player),',') as players_in_game
                       FROM matches
                       WHERE tournament_id = (%s)
                       GROUP BY matches.match;''', (t_id,))
    matches = cur.fetchall()
    conn.close()
    return matches

def swissPairings(tournament='default'):
    """
        Returns a list of pairs of players for the next round of a match.
  
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
    matches = _generate_match_history(tournament)
    # TODO : Handle case when match history is empty
    # matches should return (player_id, winner, match)
    # returns [(1, True, 1), (2, False, 1), (3, False, 2), (4, True, 2), (1, True, 3), (4, False, 3), (2, False, 4), (3, True, 4)]

    for standing in standings:
        G.add_node(standing[0],
                   name=standing[1],
                   win=standing[2],
                   matches=standing[3])
    # G.nodes() returns [1,2,3....]
    # G.node[1] returns {'name': 'p1', 'matches': 2, 'win': 2}
    players, plays = _generate_players_games_played(standings, matches)
    # plays returns : {1: {2, 4}, 2: {1}, 3: {4}, 4: {1, 3}}
    # Creates an undirected graph of players who have not played against each other
    for player in players:
        not_played = players - set(plays[player]) - {player}
        # print(not_played) returns {3}, {3,4}, {1,2},{2}
        # print(list(zip([player] * len(not_played), not_played))) returns [(1, 3)], [(2, 3), (2, 4)], [(3, 1), (3, 2)], [(4, 2)]
        weights = list(map(lambda x: abs(G.node[x]['win']+G.node[player]['win'] + 1), not_played))
        G.add_weighted_edges_from(list(zip([player] * len(not_played), not_played, weights)))

    res = nx.algorithms.max_weight_matching(G)
    # remove duplicates
    keys = res.keys()
    for key in list(keys):
        if key in res:
            del res[res[key]]
    # Convert into tuple pairs
    names = {tup[0]:tup[1] for tup in standings}

    results = [(key, names[key], res[key], names[res[key]]) for key in res]

    return results