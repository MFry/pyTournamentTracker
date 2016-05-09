#!/usr/bin/env python
"""
    Sample code usage of the pyTournamentTracker
"""

from tournament import *


def initial_setup():
    """
        Deletes the players and matches for a clean start
    """
    delete_matches()
    delete_players()


def basic_usage():
    """
    Basic usage of the pyTournamentTracker library

    """
    print('Sample Usage of the python Tournament Tracker')
    answer = input('Register(r) players manually or add default(d) players? (r/d): ')
    if answer.lower() == 'd':
        p_id = register_player('Player 1')
        print('Registered: Player 1 as {}'.format(p_id))
        p_id = register_player('Player 2')
        print('Registered: Player 2 as {}'.format(p_id))
        p_id = register_player('Player 3')
        print('Registered: Player 3 as {}'.format(p_id))
        p_id = register_player('Player 4')
        print('Registered: Player 4 as {}'.format(p_id))
        print('Total Players registered: {}'.format(count_players()))
    elif answer.lower() == 'r':
        total_players = input('How many players would you like to register?')
        for i in range(int(total_players)):
            name = input('Player name: ')
            p_id = register_player(name)
            print('Registered: {} as {}'.format(name, p_id))
    else:
        exit('Invalid command {}'.format(answer))
    print('\nNOTE: Report match by ID given.\n')
    while True:
        print('Initial Player standings')
        standings = player_standings()
        for s in standings:
            print('Player: {}  ID: {} -- Games Played: {} -- Wins: {}'.format(s[1], s[0], s[3], s[2]))
        while True:
            match_cont = input('Report match: (y/n): ')
            if match_cont.lower() == 'y':
                winner = input('Match winner: ')
                loser = input('Match loser: ')
                report_match({winner: True, loser: False})
                report = swiss_pairings()
                print('Current valid pairings: ')
                for r in report:
                    print('Valid pairing: {}, ID: {} - {}, ID: {}'.format(r[1], r[0], r[3], r[2]))
            else:
                break

        print('Current Standings')
        standings = player_standings()
        for s in standings:
            print('Player: {} -- ID: {} -- Games Played: {} -- Wins: {}'.format(s[1], s[0], s[3], s[2]))
        cont = input('Continue: (y/n)')
        if cont.lower() == 'y':
            continue
        else:
            break


if __name__ == '__main__':
    initial_setup()
    basic_usage()
