#! /usr/bin/env python3.3

import rank
from rank import Team, Player, p_iq


class PlayerDict:
    def __init__(self):
        self.ps = {}


    def add_player(self, name):
        p = Player(name);
        self.ps[name] = p
        return p

    def player(self, name):
        return self.ps[name]

    def update_player(self, p):
        self.ps[p.name] = p


class TeamDict:
    def __init__(self, pdict):
        self.ts = {}
        self.ps = pdict

    def add_team(self, tname, pnames):
        t = Team(tname, [self.ps.add_player(x) for x in pnames])
        self.ts[tname] = t
        return t

    def team(self, tname):
        return self.ts[tname]

    def update_team(self, t):
        for p in t.players:
            self.ps.update_player(p)
        self.ts[t.name] = t

    def __getattr__(self, attr):
        return self.team(attr)


    def stats(self):
        return ' '.join([repr(x) for x in sorted(self.ts.itervalues(), key=lambda x: x.name)])






def initial_state():
    ps = PlayerDict()
    ts = TeamDict(ps)
    ts.add_team('clg', ['hotshotgg', 'chauster', 'link', 'doublelift', 'aphromoo'])
    ts.add_team('tsm', ['chaox', 'reginald', 'dyrus', 'xpecial', 'theoddone'])
    ts.add_team('crs', ['saintvicious', 'cop', 'voyboy', 'nyjacky', 'elementz'])
    ts.add_team('dig', ['scarra', 'patoy', 'imaqtpie', 'crumbzz', 'kiwikid'])
    ts.add_team('ggu', ['zionspartan', 'nintendudex', 'shiphtur', 'dontmashme', 'iamanjo'])
    ts.add_team('vul', ['mandatorycloud', 'muffinqt', 'sychosid', 'xmithie', 'zuna'])
    ts.add_team('mrn', ['megazero', 'clakeyd', 'ecco', 'heartbeat', 'atomicn'])
    ts.add_team('col', ['nickwu', 'lautemortis', 'chuuper', 'brunchu', 'meyea'])

    return (ps, ts)


def match(ts, winner, loser):
    win_prob = rank.p_iqfull(rank.beta, winner, loser)
    if win_prob < 0.15:
        print('Crazy result: {0} beats {1} at odds of {2:0.2}'.format(repr(winner), repr(loser), win_prob))
    elif win_prob < 0.30:
        print('Upset: {0} beats {1} at odds of {2:0.2}'.format(repr(winner), repr(loser), win_prob))
    ranks = {winner: 1, loser: 2}
    (winner_after, loser_after) = rank.update_bt_full(rank.beta, [winner, loser], ranks)
    ts.update_team(winner_after)
    ts.update_team(loser_after)




def week1(ts):
    match(ts, ts.clg, ts.tsm)
    match(ts, ts.crs, ts.dig)
    match(ts, ts.clg, ts.ggu)
    match(ts, ts.tsm, ts.vul)
    match(ts, ts.crs, ts.clg)
    match(ts, ts.tsm, ts.dig)
    match(ts, ts.crs, ts.ggu)
    match(ts, ts.dig, ts.vul)

def week2(ts):
    match(ts, ts.dig, ts.mrn)
    match(ts, ts.tsm, ts.vul)
    match(ts, ts.crs, ts.col)
    match(ts, ts.dig, ts.tsm)
    match(ts, ts.crs, ts.vul)
    match(ts, ts.dig, ts.ggu)
    match(ts, ts.tsm, ts.mrn)
    match(ts, ts.ggu, ts.vul)

def week3(ts):
    match(ts, ts.vul, ts.clg)
    match(ts, ts.crs, ts.ggu)
    match(ts, ts.dig, ts.clg)
    match(ts, ts.vul, ts.col)
    match(ts, ts.mrn, ts.ggu)
    match(ts, ts.clg, ts.col)
    match(ts, ts.vul, ts.mrn)
    match(ts, ts.col, ts.ggu)

def week4(ts):
    match(ts, ts.clg, ts.vul)
    match(ts, ts.crs, ts.mrn)
    match(ts, ts.tsm, ts.col)
    match(ts, ts.clg, ts.ggu)
    match(ts, ts.crs, ts.col)
    match(ts, ts.tsm, ts.ggu)
    match(ts, ts.dig, ts.vul)
    match(ts, ts.mrn, ts.clg)
    match(ts, ts.dig, ts.crs)
    match(ts, ts.vul, ts.col)
    match(ts, ts.dig, ts.ggu)
    match(ts, ts.mrn, ts.tsm)
    match(ts, ts.tsm, ts.vul)
    match(ts, ts.dig, ts.col)
    match(ts, ts.mrn, ts.ggu)
    match(ts, ts.clg, ts.crs)
    match(ts, ts.crs, ts.tsm)
    match(ts, ts.clg, ts.col)
    match(ts, ts.dig, ts.mrn)
    match(ts, ts.ggu, ts.vul)

def week5(ts):
    match(ts, ts.tsm, ts.ggu)
    match(ts, ts.col, ts.dig)
    match(ts, ts.crs, ts.clg)
    match(ts, ts.vul, ts.mrn)
    match(ts, ts.crs, ts.tsm)
    match(ts, ts.dig, ts.ggu)
    match(ts, ts.col, ts.vul)
    match(ts, ts.clg, ts.mrn)
    match(ts, ts.tsm, ts.col)
    match(ts, ts.vul, ts.dig)
    match(ts, ts.ggu, ts.clg)
    match(ts, ts.crs, ts.mrn)

def week6(ts):
    match(ts, ts.dig, ts.mrn)
    match(ts, ts.tsm, ts.col)
    match(ts, ts.dig, ts.clg)
    match(ts, ts.tsm, ts.mrn)
    match(ts, ts.tsm, ts.clg)
    match(ts, ts.mrn, ts.col)
    match(ts, ts.vul, ts.clg)
    match(ts, ts.dig, ts.col)

def week7(ts):
    match(ts, ts.tsm, ts.clg)
    match(ts, ts.crs, ts.dig)
    match(ts, ts.ggu, ts.vul)
    match(ts, ts.col, ts.mrn)
    match(ts, ts.dig, ts.tsm)
    match(ts, ts.clg, ts.crs)
    match(ts, ts.mrn, ts.vul)
    match(ts, ts.ggu, ts.col)
    match(ts, ts.dig, ts.mrn)
    match(ts, ts.clg, ts.col)
    match(ts, ts.tsm, ts.ggu)
    match(ts, ts.crs, ts.vul)

def week8(ts):
    match(ts, ts.col, ts.clg)
    match(ts, ts.crs, ts.ggu)
    match(ts, ts.vul, ts.tsm)
    match(ts, ts.mrn, ts.col)
    match(ts, ts.tsm, ts.crs)
    match(ts, ts.col, ts.vul)
    match(ts, ts.ggu, ts.mrn)
    match(ts, ts.crs, ts.vul)

def week9(ts):
    match(ts, ts.crs, ts.mrn)
    match(ts, ts.clg, ts.dig)
    match(ts, ts.crs, ts.col)
    match(ts, ts.ggu, ts.mrn)
    match(ts, ts.ggu, ts.dig)
    match(ts, ts.mrn, ts.clg)
    match(ts, ts.ggu, ts.col)
    match(ts, ts.tsm, ts.crs)

def week10(ts):
    match(ts, ts.col, ts.dig)
    match(ts, ts.tsm, ts.mrn)
    match(ts, ts.col, ts.ggu)
    match(ts, ts.tsm, ts.clg)
    match(ts, ts.ggu, ts.crs)
    match(ts, ts.clg, ts.dig)
    match(ts, ts.vul, ts.mrn)
    match(ts, ts.tsm, ts.col)
    match(ts, ts.crs, ts.mrn)
    match(ts, ts.vul, ts.ggu)
    match(ts, ts.dig, ts.crs)
    match(ts, ts.clg, ts.vul)
    match(ts, ts.mrn, ts.clg)
    match(ts, ts.col, ts.crs)
    match(ts, ts.tsm, ts.ggu)
    match(ts, ts.dig, ts.vul)
    match(ts, ts.ggu, ts.clg)
    match(ts, ts.tsm, ts.dig)
    match(ts, ts.mrn, ts.col)
    match(ts, ts.vul, ts.crs)

def playoffs(ts):
    match(ts, ts.ggu, ts.dig)
    match(ts, ts.vul, ts.clg)
    match(ts, ts.tsm, ts.vul)
    match(ts, ts.ggu, ts.crs)
    match(ts, ts.vul, ts.crs)
    match(ts, ts.tsm, ts.ggu)

def do():
    ps, ts = initial_state()
    weeks = [week1, week2, week3, week4, week5, week6, week7, week8, week9, week10, playoffs]
    print(ts.stats())
    for w in weeks:
        print('')
        w(ts)
        print(ts.stats())
    


if __name__ == '__main__':
    do()