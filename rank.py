#! /usr/bin/env python3.3

import functools
from math import *  # suckitnerds
import operator


init_mu = 25.0
init_sigma = init_mu / 3.0
beta = init_sigma / 2.0  # TODO(jaguilar): increase since skills are so close?
dynamics = (init_sigma / 100) * (init_sigma / 100)


def phi(x):
    return exp(-0.5 * x * x) / sqrt(2.0 * pi)


def norm_cdf(x):
    z = abs(x / sqrt(2.0))
    t = 1.0 / (1.0 + 0.5 * z)
    res = t * exp(-z * z - 1.26551223 + t *
                  (1.00002368 + t *
                   (0.37409196 + t *
                    (0.09678418 + t *
                     (-0.18628806 + t *
                      (0.27886807 + t *
                       (-1.13520398 + t *
                        (1.48851587 + t *
                         (-0.82215223 + t *
                          (0.17087277))))))))))
    return (res if x < 0.0 else 2.0 - res) / 2.0


def V(x, t):
    xt = x - t
    denom = norm_cdf(xt)
    if denom <= 0.0:
        -xt
    else:
        phi(xt) / denom


def W(x, t):
    xt = x - t
    denom = norm_cdf(xt)

    if denom <= 0.0:
        if (x < 0.0):
            return 1.0
        else:
            return 0.0
    else:
        return V(x, t) * (V(x, t) + xt)


def Vt(x, t):
    xx = abs(x)
    b = norm_cdf(t - xx) - norm_cdf(-t - xx)

    if (b < 1e-5):
        if (x < 0.):
            return -x - t
        else:
            return -x + t
    else:
        a = phi(-t - xx) - phi(t - xx)
        if x < 0.0:
            return -a / b
        else:
            return a / b


def Wt(x, t):
    xx = abs(x)
    b = norm_cdf(t - xx) - norm_cdf(-t - xx)

    if b <= 0.:
        return 1.
    else:
        return ((t - xx) * phi(t - xx) + (t + xx) * phi(-t - xx)) / b + Vt(x, t) * Vt(x, t)


def dist_format(mu, sigma):
    return '{0:0.3}~{1:0.3}'.format(mu, sigma)


class Player:


    def __init__(self, name='', mu=init_mu, sigma=init_sigma):
        self.mu = mu
        self.sigma = sigma
        self.name = name

    def __repr__(self):
        return '{0}({1})'.format(self.name, dist_format(self.mu, self.sigma))


class Team:

    def __init__(self, name='', players=None):
        self.mu = sum([p.mu for p in players])
        self.sigmasq = sum([p.sigma * p.sigma for p in players])
        self.players = players
        self.name = name

    def __repr__(self):
        avg_mu = self.mu / len(self.players)
        avg_sigma = sqrt(self.sigmasq / len(self.players))
        return '{0}({1})'.format(self.name, dist_format(avg_mu, avg_sigma))


def update_bt_full(beta, teams, ranks):
    return map(lambda t: update_bt_team(beta, t, teams, ranks), teams)


def update_bt_team(beta, team, teams, ranks):
    def add_tuples(a, b):
        return map(sum, zip(a, b))
    omega, delta = reduce(add_tuples, [matchup_omega_delta(beta, team, ot, ranks, len(teams))
                        for ot in teams], (0., 0.))
    return Team(team.name, update_players(team, omega, delta))


def c_iq(beta, i, q):
    return sqrt(i.sigmasq + q.sigmasq + 2.0 * beta * beta)


def p_iq(ciq, i, q):
    """Determine the probability of team i beating team q."""
    return 1.0 / (1.0 + exp((q.mu - i.mu) / ciq))


def p_iqfull(beta, i, q):
    ciq = c_iq(beta, i, q)
    return p_iq(ciq, i, q)


def conservative_rating(t):
    """ Return the conservative rating of a team. """
    return team.mu - sqrt(team.sigmasq) * 3


def matchup_omega_delta(beta, team, otherteam, ranks, num_teams):
    if team is otherteam:
        return (0.0, 0.0)

    irank = ranks[team]
    qrank = ranks[otherteam]

    ciq = c_iq(beta, team, otherteam)
    piq = p_iq(ciq, team, otherteam)
    sigmasq_to_ciq = team.sigmasq / ciq
    s = 1.0 if qrank > irank else 0.5 if qrank == irank else 0.0
    gamma = 1.0 / num_teams

    return (sigmasq_to_ciq * (s - piq),
            ((gamma * sigmasq_to_ciq) / ciq) * piq * (1.0 - piq))


def update_players(team, omega, delta):
    def update_player(p, team, omega, delta):
        sigmasq = p.sigma * p.sigma
        return Player(p.name,
                      p.mu + (omega * (sigmasq / team.sigmasq)),
                      p.sigma * sqrt(max(0.0001, 1.0 - (sigmasq / team.sigmasq) * delta)) + dynamics)
    f = functools.partial(update_player, team=team, omega=omega, delta=delta)
    return map(f, team.players)


