#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


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
        cur.execute('SELECT id FROM tournaments where name = (%s);', (tournament,))
        tournament_id = cur.fetchone()[0]
        cur.execute('DELETE FROM matches WHERE t_id = (%s)', (tournament_id,))
    else:
        cur.execute('DELETE FROM matches;')
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM players;')
    cur.execute('DELETE FROM tournament_players;')
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
    cur.execute('SELECT tournament_name, total_players FROM view_tournament_size;')
    tournaments_player_count = cur.fetchall()
    print(tournaments_player_count)
    return tournaments_player_count


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
    print(standings)
    conn.close()

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
    standings = playerStandings(tournament)
    con = connect()
    cur = con.cursor()
    t_id = getTournament(tournament)
    cur.execute('SELECT * FROM matches WHERE t_id = (%s);', (t_id,))
    matches = cur.fetchall
    # TODO: Implement strong-weak pairing matching problem
    '''
    Create a graph with all players in current point total
    Connect players in the graph that have not played yet
    Use a Blossom based algorithm to compute a maximal matching of the graph
    Take any unpaired players and add them to the group with the next highest point total
    '''


#registerTournament('default')
#print(getTournament('default'))
#print(getTournament('tournament1'))
print(playerStandings('tournament1'))
#reportMatch({1:'True', 2:'False'}, tournament='tournament1')
#registerPlayer('Steve Bobs')
#registerPlayer('Michal Frystacky')
#registerPlayer('Steve Davies')
#registerPlayer('test3')
#countPlayers()
#deleteMatches(tournament='tournament1')
#deleteMatches()