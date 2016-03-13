-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT);

-- VIEW FOR PLAYER PARTICULAR TOURNAMENT AND THEIR STATS

-- TOURNAMENT : PAIR UP PLAYERS
CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY ,
  name TEXT);

CREATE TABLE tournament (
  td INTEGER REFERENCES tournaments(id),
  match SERIAL,
  player_1 INTEGER REFERENCES players(id),
  player_2 INTEGER REFERENCES players(id),
  winner INTEGER REFERENCES players(id),
  PRIMARY KEY (td, match));