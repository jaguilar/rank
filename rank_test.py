#! /usr/bin/env python3.3

import rank
import unittest


class TheTest(unittest.TestCase):

    def test_normcdf(self):
        self.assertAlmostEqual(0.93319279, rank.norm_cdf(1.5))

    def test_rank(self):
        team1 = rank.Team('tsm', [rank.Player()])
        team2 = rank.Team('clg', [rank.Player()])
        print([team1, team2])
        print(rank.p_iq(rank.c_iq(rank.beta, team1, team2), team1, team2))
        team1p, team2p = rank.update_bt_full(rank.beta, [team1, team2], {team1: 1, team2: 2})
        print([team1p, team2p])
        print(rank.p_iq(rank.c_iq(rank.beta, team1p, team2p), team1p, team2p))

if __name__ == '__main__':
    unittest.main()
