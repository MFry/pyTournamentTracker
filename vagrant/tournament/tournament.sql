-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  id   SERIAL PRIMARY KEY NOT NULL,
  name TEXT               NOT NULL);

-- VIEW FOR PLAYER PARTICULAR TOURNAMENT AND THEIR STATS
CREATE TABLE tournament_players (
  player_id INTEGER REFERENCES players(id)         NOT NULL,
  tournament_id INTEGER REFERENCES tournaments(id) NOT NULL,
  PRIMARY KEY (player_id, tournament_id));

-- TOURNAMENT : PAIR UP PLAYERS
CREATE TABLE tournaments (
  id   SERIAL PRIMARY KEY NOT NULL,
  name TEXT               NOT NULL);

CREATE TABLE tournament (
  t_id     INTEGER REFERENCES tournaments(id) NOT NULL,
  match    SERIAL                             NOT NULL,
  player_1 INTEGER REFERENCES players(id),
  player_2 INTEGER REFERENCES players(id),
  winner   INTEGER REFERENCES players(id),
  PRIMARY KEY (td, match));

CREATE VIEW tournament_size as
  SELECT tournament_id, count(*) as total_players
  FROM tournament_players
  GROUP BY tournament_id;
