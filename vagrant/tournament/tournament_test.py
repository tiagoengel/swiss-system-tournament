#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def test_count():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    delete_all_matches()
    delete_tournaments()
    delete_all_players()
    c = count_all_players()
    if c == '0':
        raise TypeError(
            "count_all_players should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, count_all_players should return zero.")  # noqa
    print "1. count_all_players() returns 0 after initial delete_all_players() execution."  # noqa
    register_player("Chandra Nalaar")
    c = count_all_players()
    if c != 1:
        raise ValueError(
            "After one player registers, count_all_players() should be 1. Got {c}"  # noqa
            .format(c=c))
    print "2. count_all_players() returns 1 after one player is registered."
    register_player("Jace Beleren")
    c = count_all_players()
    if c != 2:
        raise ValueError(
            "After two players register, count_all_players() should be 2. Got {c}"  # noqa
            .format(c=c))
    print "3. count_all_players() returns 2 after two players are registered."
    delete_all_players()
    c = count_all_players()
    if c != 0:
        raise ValueError(
            "After deletion, count_all_players should return zero.")
    print "4. count_all_players() returns zero after registered players are deleted."  # noqa
    print "5. Player records successfully deleted."

    register_player("Jace Beleren")
    register_tournament("Counting contest")
    register_tournament("Backwards running contest")
    [(tid1, tname1), (tid2, tname2)] = list_tournaments()
    register_all_players_into(tid1)

    register_player("Chandra Nalaar")
    register_all_players_into(tid2)

    c = count_players(tid1)
    if c != 1:
        raise ValueError(
            "After one player register, count_players() should be 1 for "
            "the first contest. Got {c}"
            .format(c=c))

    c = count_players(tid2)
    if c != 2:
        raise ValueError(
            "After two players register, count_players() should be 2 for "
            "the second contest. Got {c}"
            .format(c=c))

    print "6. count_players() returns the right amount of players in each tournament."  # noqa
    delete_players(tid1)
    c = count_players(tid1)
    if c != 0:
        raise ValueError(
            "After deletion, count_all_players should return zero."
            "the first contest. Got {c}"
            .format(c=c))

    delete_players(tid2)
    c = count_players(tid2)
    if c != 0:
        raise ValueError(
            "After deletion, count_all_players should return zero."
            "the first contest. Got {c}"
            .format(c=c))

    print "7. delete_players() remove players from the right tournament."


def test_register_tournaments():
    """Test tournaments registration."""
    delete_tournaments()
    register_tournament("Ping Pong masters")
    register_tournament("Chess")

    all_tournaments = list_tournaments()
    if len(all_tournaments) != 2:
        raise ValueError(
            "Expect two tournaments but got %s " % (len(all_tournaments)))

    delete_tournaments()

    if len(list_tournaments()) != 0:
        raise ValueError(
            "After deletion, list_tournaments should return zero")

    print "8. test_register_tournaments() register and deletes tournaments correctly."  # noqa


def test_standings_before_matches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    delete_all_matches()
    delete_tournaments()
    delete_all_players()
    register_player("Melpomene Murray")
    register_player("Randy Schwartz")
    [(p1, p1name), (p2, p2name)] = list_players()
    register_tournament("Coding tournament")
    [(tid, tname)] = list_tournaments()
    register_player_into_tournament(tid, p1)
    register_player_into_tournament(tid, p2)
    standings = player_standings(tid)
    if len(standings) < 2:
        raise ValueError(
            "Players should appear in player_standings even before "
            "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each player_standings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError(
            "Registered players' names should appear in standings, "
            "even if they have no matches played.")
    print "9. Newly registered players appear in the standings with no matches."  # noqa


def test_report_matches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    delete_all_matches()
    delete_tournaments()
    delete_all_players()
    register_player("Bruno Walton")
    register_player("Boots O'Neal")
    register_player("Cathy Burton")
    register_player("Diane Grant")
    register_tournament("Spit contest")
    [(tid, tname)] = list_tournaments()
    register_all_players_into(tid);
    standings = player_standings(tid)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(tid, id1, id2)
    report_match(tid, id3, id4)
    standings = player_standings(tid)

    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError(
                "Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError(
                "Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "10. After a match, players have updated standings."

    delete_all_matches()
    standings = player_standings(tid)
    if len(standings) != 4:
        raise ValueError(
            "Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError(
                "After deleting matches, players should have zero matches recorded.")  # noqa
        if w != 0:
            raise ValueError(
                "After deleting matches, players should have zero wins recorded.")  # noqa
    print "11. After match deletion, player standings are properly reset."
    print "12. Matches are properly deleted."


def test_pairings():
    """Test that pairings are generated properly both before and after match reporting."""  # noqa
    delete_all_matches()
    delete_tournaments()
    delete_all_players()
    register_player("Twilight Sparkle")
    register_player("Fluttershy")
    register_player("Applejack")
    register_player("Pinkie Pie")
    register_player("Rarity")
    register_player("Rainbow Dash")
    register_player("Princess Celestia")
    register_player("Princess Luna")
    register_tournament("FFC - Finger Fighting Championship")
    [(tid, tname)] = list_tournaments()
    register_all_players_into(tid);
    standings = player_standings(tid)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swiss_pairings(tid)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swiss_pairings should return 4 pairs. Got {pairs}"  # noqa
            .format(pairs=len(pairings)))

    report_match(tid, id1, id2)
    report_match(tid, id3, id4)
    report_match(tid, id5, id6)
    report_match(tid, id7, id8)
    pairings = swiss_pairings(tid)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swiss_pairings should return 4 pairs. Got {pairs}"  # noqa
            .format(pairs=len(pairings)))

    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([
        frozenset([pid1, pid2]),
        frozenset([pid3, pid4]),
        frozenset([pid5, pid6]),
        frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "13. After one match, players with one win are properly paired."


def test_parings_using_points():
    """Test that parings are made using both the wins and the user's points.

    Points are given to an user in every match and are related to the amount of
    wins the opponent has, thus given more value too a win over a better
    oppenent.
    """
    delete_all_matches()
    delete_tournaments()
    delete_all_players()

    [register_player(p) for p in ["A", "B", "C", "D", "E", "F", "G", "H"]]

    register_tournament("Spelling contest")
    [(tid, tname)] = list_tournaments()
    register_all_players_into(tid)

    standings = player_standings(tid)
    [a, b, c, d, e, f, g, h] = [row[0] for row in standings]

    report_match(tid, a, b)
    report_match(tid, c, d)
    report_match(tid, e, f)
    report_match(tid, g, h)

    report_match(tid, a, c)
    report_match(tid, e, g)
    report_match(tid, b, d)
    report_match(tid, f, h)

    # Porpuselly match the games in the wrong order
    # to test the parings
    report_match(tid, b, a)
    report_match(tid, f, e)
    report_match(tid, c, d)
    report_match(tid, g, h)

    # After this A, B, E and F should have 2 wins each but
    # B and E should have more points, thus they need to be
    # paired for the next match
    pairings = [set([p[1], p[3]]) for p in swiss_pairings(tid)]

    if not set(["B", "F"]) in pairings:
        raise ValueError(
            "B and E should've been paired")

    if not set(["A", "E"]) in pairings:
        raise ValueError(
            "A and F should've been paired")

    print "14. Wins over players with more wins should have more value."


def test_multiple_tournaments():
    """System should handle multiple tournaments.

    Results from one tournament should not interfer on others and
    users should be allowed to participate in more than one tournament
    at the same time.
    """
    delete_all_matches()
    delete_tournaments()
    delete_all_players()

    [register_player(p) for p in ["A", "B", "C", "D", "E", "F", "G", "H"]]

    register_tournament("Bad jokes contest")
    register_tournament("Selfie contest")

    [(tid1, tname1), (tid2, tname2)] = list_tournaments()

    all_players = list_players()
    selfie_contestants = all_players[0:4]

    [(id1, name1),
     (id2, name2),
     (id3, name3),
     (id4, name4),
     (id5, name5),
     (id6, name6),
     (id7, name7),
     (id8, name8)] = all_players

    [register_player_into_tournament(tid1, p[0]) for p in all_players]
    [register_player_into_tournament(tid2, p[0]) for p in selfie_contestants]

    t1_standings = player_standings(tid1)
    if len(t1_standings) != 8:
        raise ValueError("Bad jokes contest should have 8 players standing")

    t2_standings = player_standings(tid2)
    if len(t1_standings) != 8:
        raise ValueError("Selfie contest should have 4 players standing")

    t1_pairings = swiss_pairings(tid1)
    if len(t1_pairings) != 4:
        raise ValueError(
            "Bad jokes parings should return 4 pairs.")

    t2_pairings = swiss_pairings(tid2)
    if len(t2_pairings) != 2:
        raise ValueError(
            "Selfie parings should return 2 pairs.")

    print "15. Parings with multiple tournaments should work."

    report_match(tid1, id1, id2)
    report_match(tid1, id3, id4)
    report_match(tid1, id5, id6)
    report_match(tid1, id7, id8)

    report_match(tid1, id1, id3)
    report_match(tid1, id5, id7)
    report_match(tid1, id2, id4)
    report_match(tid1, id6, id8)

    report_match(tid2, id2, id1)
    report_match(tid2, id4, id3)

    test_standings(tid1, "Bad jokes contest", set([
        (id1, name1, 2, 2),
        (id2, name2, 1, 2),
        (id3, name3, 1, 2),
        (id4, name4, 0, 2),
        (id5, name5, 2, 2),
        (id6, name6, 1, 2),
        (id7, name7, 1, 2),
        (id8, name8, 0, 2)
    ]))

    t2_expected_status = set([
        (id1, name1, 0, 1),
        (id2, name2, 1, 1),
        (id3, name3, 0, 1),
        (id4, name4, 1, 1)
    ])
    test_standings(tid2, "Selfie contest", t2_expected_status)

    print "16. Matches result from one tournament should not interfere in the others."  # noqa

    delete_matches(tid1)
    test_standings(tid2, "Selfie contest", t2_expected_status)

    print "17. Removing matches from one tournament should not interfere in the others."  # noqa


def test_report_winner():
    delete_all_matches()
    delete_tournaments()
    delete_all_players()

    [register_player(p) for p in ["A", "B", "C", "D"]]

    register_tournament("Go tournament")
    [(tid1, tname1)] = list_tournaments()
    register_all_players_into(tid1)

    standings = player_standings(tid1)
    [id1, id2, id3, id4] = [row[0] for row in standings]

    report_match(tid1, id1, id2)
    report_match(tid1, id3, id4)

    if report_winner(tid1):
        raise ValueError(
            "Tournament should have no winner if the minimun amount "
            "of matches was not played")

    print "18. The tournament has no winner if the minimun amount of matches was not played."  # noqa

    report_match(tid1, id1, id3)
    report_match(tid1, id2, id4)

    winner = report_winner(tid1)
    if not winner:
        raise ValueError(
            "Tournament should have a winner after minimun amount "
            "of matches is played")

    if winner[0] != id1:
        raise ValueError(
            "The winner should be the player A")

    print "19. The right winner is reported."


def test_standings(tournament_id, tournament_name, expected):
    standings = player_standings(tournament_id)
    for standing in standings:
        if standing not in expected:
            raise ValueError(
                "Player %s should have %s wins and %s matches in %s"
                % (standing[1], standing[2], standing[3], tournament_name))


def register_all_players_into(tournament):
    all_players = list_players()
    for (pid, name) in all_players:
        register_player_into_tournament(tournament, pid)


if __name__ == '__main__':
    test_count()
    test_register_tournaments()
    test_standings_before_matches()
    test_report_matches()
    test_pairings()
    test_parings_using_points()
    test_multiple_tournaments()
    test_report_winner()
    print "Success!  All tests pass!"
