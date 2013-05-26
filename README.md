rank
====

This project creates skill ratings for players and teams of players. It is still in a fairly 
rudimentary state.

The output below is the rating of the various teams playing in the spring split of the LCS
for the first four weeks of play. The model of skill is a gaussian, where the mu represents
the expected performance and the sigma represents the deviation in performance. In practical
terms, this means that the mu represents "how good" the algorithm thinks the team is, and the
sigma represents how uncertain the algorithm is about its guess (and/or how consistent the team
is -- these two are more or less the same value).

The format of the following output is:

    TEAM_NAME(SIGMA~MU)
    
After four weeks, the algorithm believes Team Curse and Team Dignitas are way better than the other
teams.

```
clg(25.0~8.33) col(25.0~8.33) crs(25.0~8.33) dig(25.0~8.33) ggu(25.0~8.33) mrn(25.0~8.33) tsm(25.0~8.33) vul(25.0~8.33)
clg(26.1~6.21) col(25.0~8.33) crs(28.2~5.98) dig(23.7~6.08) ggu(23.1~6.43) mrn(25.0~8.33) tsm(25.8~6.2) vul(22.2~6.58)
clg(26.1~6.21) col(24.0~7.09) crs(28.9~4.36) dig(26.1~4.67) ggu(23.1~4.92) mrn(22.4~6.2) tsm(25.8~4.66) vul(20.9~4.1)
clg(24.3~3.99) col(22.5~4.48) crs(29.1~3.6) dig(26.6~4.22) ggu(22.0~3.39) mrn(22.4~4.62) tsm(25.8~4.66) vul(22.6~3.35)
clg(25.1~1.52) col(22.1~0.556) crs(28.6~1.52) dig(27.7~0.0157) ggu(21.7~1.51) mrn(23.5~1.14) tsm(25.6~1.98) vul(22.1~2.03)
```
