#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class new_transaction:
    def __enter__(self):
        self.db = connect()
        self.cr = self.db.cursor()
        return self.cr

    def __exit__(self, type, value, traceback):
        self.db and self.db.commit()
        self.cr and self.cr.close()
        self.db and self.db.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    with new_transaction() as cr:
        cr.execute("delete from matches")


def deletePlayers():
    """Remove all the player records from the database."""
    with new_transaction() as cr:
        cr.execute("delete from players")


def countPlayers():
    """Returns the number of players currently registered."""
    with new_transaction() as cr:
        cr.execute("select count(*) from players")
        return cr.fetchone()[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with new_transaction() as cr:
        query = "insert into players ( name ) values ( %s )"
        cr.execute(query, (name,))


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
    with new_transaction() as cr:
        cr.execute("""
        select id, name, wins, matches from player_status as player
        where not exists (
            select 1 from matches where player = player.id and won is null
        )
        """)
        return cr.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with new_transaction() as cr:
        query = """insert into
                   matches ( player, opponent, won, points )
                   values ( %s, %s, %s, %s )"""

        # The winner receives as points the ammount of wins the loser has plus
        # one. This will give more value to a win over a player that has won
        # more matches and the amount of points a user has can be used to find
        # the best match and the winner in case of ties.
        cr.execute("select wins from player_status where id = %s", (loser,))
        loser_wins = cr.fetchone()[0]
        p = loser_wins + 1
        params = ((winner, loser, 1, p,),
                  (loser, winner, 0, 0,))
        cr.executemany(query, params)


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
    players = playerStandings()

    def create_pair(idx):
        p1 = players[idx]
        p2 = players[idx+1]
        return (p1[0], p1[1], p2[0], p2[1])

    return [create_pair(i) for i in xrange(0, len(players), 2)]

