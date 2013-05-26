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
> python rank_data.py 

clg(25.0~8.33) col(25.0~8.33) crs(25.0~8.33) dig(25.0~8.33) ggu(25.0~8.33) mrn(25.0~8.33) tsm(25.0~8.33) vul(25.0~8.33)

clg(26.0~8.21) col(25.0~8.33) crs(28.5~8.21) dig(24.0~8.21) ggu(23.0~8.25) mrn(25.0~8.33) tsm(26.2~8.21) vul(22.2~8.25)

clg(26.0~8.21) col(24.1~8.29) crs(29.8~8.15) dig(27.6~8.09) ggu(23.3~8.18) mrn(22.5~8.25) tsm(26.6~8.09) vul(19.8~8.15)
Upset: vul(19.8~8.15) beats clg(26.0~8.21) at odds of 0.236274733992

clg(24.4~8.1) col(22.6~8.17) crs(30.4~8.13) dig(28.5~8.05) ggu(20.2~8.07) mrn(22.5~8.16) tsm(26.6~8.09) vul(24.5~8.04)
Upset: clg(24.6~8.0) beats crs(29.7~8.05) at odds of 0.27108278741
Upset: ggu(18.3~7.98) beats vul(22.8~7.9) at odds of 0.297238518341

clg(26.9~7.94) col(19.5~8.03) crs(29.1~7.98) dig(31.8~7.93) ggu(20.1~7.95) mrn(25.4~8.01) tsm(26.0~7.92) vul(21.1~7.86)
Crazy result: col(19.5~8.03) beats dig(31.8~7.93) at odds of 0.084
Upset: vul(21.4~7.79) beats dig(29.9~7.91) at odds of 0.160131964264
Upset: ggu(19.2~7.91) beats clg(26.9~7.86) at odds of 0.180824378422

clg(24.9~7.84) col(22.2~7.95) crs(31.3~7.88) dig(27.8~7.89) ggu(21.2~7.88) mrn(22.3~7.92) tsm(26.6~7.83) vul(23.4~7.78)

clg(22.2~7.74) col(19.8~7.86) crs(31.3~7.88) dig(29.6~7.81) ggu(21.2~7.88) mrn(22.3~7.83) tsm(28.7~7.74) vul(24.6~7.74)
Crazy result: clg(21.7~7.71) beats crs(32.3~7.84) at odds of 0.11

clg(24.5~7.67) col(19.5~7.75) crs(30.5~7.81) dig(30.3~7.72) ggu(23.1~7.78) mrn(21.8~7.73) tsm(28.7~7.64) vul(21.2~7.65)
Upset: col(19.5~7.75) beats clg(24.5~7.67) at odds of 0.267593481882
Upset: vul(21.2~7.65) beats tsm(28.7~7.64) at odds of 0.183684647058

clg(22.8~7.64) col(21.7~7.64) crs(29.7~7.74) dig(30.3~7.72) ggu(23.9~7.72) mrn(21.7~7.65) tsm(28.4~7.59) vul(21.2~7.58)
Upset: clg(22.8~7.64) beats dig(30.3~7.72) at odds of 0.183009524539
Upset: mrn(20.5~7.6) beats clg(24.7~7.62) at odds of 0.297302803968

clg(23.1~7.59) col(20.7~7.6) crs(29.0~7.67) dig(26.8~7.66) ggu(27.0~7.62) mrn(22.1~7.57) tsm(29.8~7.56) vul(21.2~7.58)
Upset: col(20.7~7.6) beats dig(26.8~7.66) at odds of 0.227062771505
Upset: col(22.5~7.57) beats ggu(27.0~7.62) at odds of 0.286838238108
Upset: vul(22.5~7.54) beats ggu(26.9~7.56) at odds of 0.289264675817
Upset: dig(23.5~7.6) beats crs(27.9~7.61) at odds of 0.291008089899
Upset: mrn(20.0~7.49) beats clg(25.2~7.5) at odds of 0.257193929929

clg(22.5~7.43) col(23.6~7.46) crs(23.3~7.51) dig(25.5~7.51) ggu(25.7~7.47) mrn(23.3~7.43) tsm(32.2~7.45) vul(23.5~7.41)

clg(21.5~7.4) col(23.6~7.46) crs(21.6~7.44) dig(24.4~7.47) ggu(27.0~7.37) mrn(23.3~7.43) tsm(33.2~7.4) vul(25.1~7.32)
```
