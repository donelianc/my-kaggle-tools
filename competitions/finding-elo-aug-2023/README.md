Finding Elo
==============================

**Predict a chess player's FIDE Elo rating from one game**

Elite chess players are rated, ranked, analyzed, and compared in many ways. Classical methods of ranking chess players have focused on game histories, paying particular attention to the relative strength of the players involved. This includes the popular [FIDE Elo](http://en.wikipedia.org/wiki/Elo_rating_system) score, which was the focus of one of Kaggle's first ever competitions - [Elo vs. the Rest of the World](http://www.kaggle.com/c/chess).

Recent work on chess analysis has focused on intrinsic performance ratings, where one assesses skill based on the quality of decisions rather than the outcomes of games. For an example of this kind of approach, see this [draft](http://www.cse.buffalo.edu/~regan/papers/pdf/Reg12IPRs.pdf) by [Kenneth Regan](http://www.cse.buffalo.edu/~regan/). Two advantages of an intrinsic approach are an increased sample size (there are many more moves than games) and the ability to approach new challenges, such as determining whether a player is cheating by performing moves above their skill level.

This competition challenges Kagglers to determine players' FIDE Elo ratings at the time a game is played, based solely on the moves in one game. Do a player's moves reflect their absolute skill? Does the opponent matter? How closely does one game reflect intrinsic ability? How well can an algorithm do? Does computational horsepower increase accuracy? Let's find out!

You do not need to be a chess expert -- or even know how to play chess -- to attempt this competition. You do need patience and a computer that doesn't mind some heat. The dataset includes 50,000 games between elite, ranked players. As a getting-started computational bonus, Kaggle has run these games through a [chess engine](http://en.wikipedia.org/wiki/Chess_engine) to score each move.

Good luck finding Elo!