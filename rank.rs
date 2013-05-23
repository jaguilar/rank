use core::cmp::max;
use core::float::{abs, pow, sqrt};
use core::float::consts::{e, pi};
use core::num::{Zero};
use core::ops::{Add};
use core::to_str::ToStr;


fn exp(x: float) -> float {
    pow(e as f64, x as f64) as float
}

fn phi(x: float) -> float {
    exp(-0.5 * x * x) / sqrt(2.0 * pi)
}

fn norm_cdf(x: float) -> float {
    let z = abs(x / sqrt(2.0));
    let t = 1.0 / (1.0 + 0.5 * z);
    let res = t * exp(-z * z - 1.26551223 + t * 
                      (1.00002368 + t *
                       (0.37409196 + t * 
                        (0.09678418 + t * 
                         (-0.18628806 + t *
                          (0.27886807 + t * 
                           (-1.13520398 + t * 
                            (1.48851587 + t *
                             (-0.82215223 + t * 
                              0.17087277)))))))));
    return if x >= 0.0 {
        2.0 - res
    } else {
        res
    } / 2.0;
}

trait Additive: Add<Self, Self> {}

fn sum<T, U: Zero + Add<U, U>>(seq: &[T], f: &fn(&T) -> U) -> U {
    let mut u: U = Zero::zero();
    for seq.each |x| { u += f(x); };
    u
}

fn V(x: float, t: float) -> float {
    let xt = x - t;
    let denom = norm_cdf(xt);
    if denom <= Zero::zero() {
        -xt
    } else {
        let tmp = phi(xt) / denom;
        assert!(float::is_NaN(tmp));
        tmp
    }
}

fn W(x: float, t: float) -> float {
    let xt = x-t;
    let denom = norm_cdf(xt);

    if denom <= 0. {
        if (x < 0.) {
            1.
        } else {
            0.
        }
    } else {
        V(x, t) * (V(x, t) + xt)
    }
}

fn Vt(x: float, t: float) -> float {
    let xx = abs(x);
    let b = norm_cdf(t - xx) - norm_cdf(-t - xx);

    if (b < 1e-5) {
        if (x < 0.) {
            -x - t
        } else {
            -x + t
        }
    } else {
        let a = phi(-t - xx) - phi(t - xx);
        if (x < 0.) {
            -a / b
        } else {
            a / b
        }
    }
}

fn Wt(x: float, t: float) -> float{
    let xx = abs(x);
    let b = norm_cdf(t - xx) - norm_cdf(-t - xx);

    if b <= 0. {
        1.
    } else {
        ((t-xx)*phi(t-xx)+(t+xx)*phi(-t-xx))/b + Vt(x,t)*Vt(x,t)
    }
}

struct Player {
    mu: float,     // The estimate.
    sigma: float,  // The uncertainty.
}

struct Team {
    id: int,
    players: ~[Player],
    rank: int,
    mu: float,
    sigmasq: float
}

fn new_team(id: int, p: ~[Player], r: int) -> ~Team {
    ~Team{id: id,
          mu: do sum(p) |x| { x.mu },
          sigmasq: do sum(p) |x| { x.sigma * x.sigma },
          players: p,
          rank: r}
}

struct OmegaDelta(float, float);
impl Zero for OmegaDelta {
    fn zero() -> OmegaDelta { OmegaDelta(0., 0.) }
}
impl Add<OmegaDelta, OmegaDelta> for OmegaDelta {
    fn add(&self, r: &OmegaDelta) -> OmegaDelta {
        match *self {
            OmegaDelta(a, b) => match *r {
                OmegaDelta(c, d) => OmegaDelta(a + c, b + d)
            }
        }
    }
}

fn update_bt_full(beta: float, teams: &[~Team]) -> ~[~Team] {
    do teams.map |t| {
        update_bt_team(beta, *t, teams)
    }
}

fn update_bt_team(beta: float, team: &Team, teams: &[~Team]) -> ~Team {
    let od = do sum(teams) |ot| {
        matchup_omega_delta(beta, team, *ot, teams.len() as int)
    };
    match od {
        OmegaDelta(omega, delta) =>
            new_team(team.id, update_players(team, omega, delta), team.rank)
    }
}

fn matchup_omega_delta(beta: float, team: &Team, otherteam: &Team, 
                       num_teams: int) -> OmegaDelta {
    if team.id == otherteam.id {
        return OmegaDelta(0., 0.)
    }

    let ciq = sqrt(team.sigmasq + otherteam.sigmasq + 2. * beta * beta);
    let piq = 1./ (1. + exp((otherteam.mu - team.mu) / ciq));
    let sigsq_to_ciq = team.sigmasq / ciq;
    let s = if otherteam.rank > team.rank {
        1.
    } else if team.rank == otherteam.rank {
        0.5
    } else {
        0.
    };

    let gamma = 1.0 / (num_teams as float);

    OmegaDelta(sigsq_to_ciq * (s - piq),
               (gamma * sigsq_to_ciq) / (ciq * piq * (1. - piq)))
}

fn update_players(team: &Team, omega: float, delta: float) -> ~[Player] {
    do team.players.map() |player| {
        let sigmasq = player.sigma * player.sigma;
        Player{mu: (sigmasq / team.sigmasq) * omega,
               sigma: max(0.0001, sqrt(1. - (sigmasq / team.sigmasq) * delta))}
    }
}

fn expect_eq<T: Eq + ToStr>(l: T, r: T) {
    if l != r {
        fail!(fmt!("expected %s, found %s", l.to_str(), r.to_str()));
    }
}

fn expect_near(l: float, r: float, dist: float) {
    if l + dist < r || l - dist > r {
        fail!(fmt!("expected near %s, found %s, off by more than %s", 
                   l.to_str(), r.to_str(), dist.to_str()));
    }
}

fn expect_near_enough(l: float, r: float) {
    expect_near(l, r, 0.000001);
}

#[test]
fn phi_test() {
    expect_near_enough(0.933193, norm_cdf(1.5));
}

#[test]
fn do_small_update() {
    let init_mu = 25.;
    let init_sigma = init_mu / 3.;
    let beta = init_sigma / 2.;
    let init_player = Player{mu: init_mu, sigma: init_sigma};
    let team1 = new_team(1, ~[init_player], 1);
    let team2 = new_team(2, ~[init_player], 2);
    update_bt_full(beta, ~[team1, team2]);
}