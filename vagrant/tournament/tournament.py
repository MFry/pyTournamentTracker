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


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM tournament;')
    conn.comit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM players;')
    conn.comit()
    conn.close()

def countPlayers():
    """
        Returns the number of players currently registered.
    :return:
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tournament_size;')
    players_count = cur.fetchall()
    print(players_count)
    return players_count # TODO: Find what should be returned.


def registerTournament(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO tournaments VALUES (%s);', (name,))
    conn.commit()
    conn.close()



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
    conn.commit()
    player_id = cur.fetchone()[0]
    cur.execute('SELECT * FROM tournaments WHERE name = (%s);', (tournament,))
    tournament_id = cur.fetchone()[1]
    print(player_id, tournament_id)
    cur.execute('INSERT INTO tournament_players VALUES (%s, %s);', (str(player_id), str(tournament_id)))
    #cur.execute('')
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

 
 
def swissPairings():
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

registerTournament('default')
registerPlayer('Steve Bobs')
registerPlayer('Michal Frystacky')
registerPlayer('Steve Davies')
registerPlayer('test3')
countPlayers()