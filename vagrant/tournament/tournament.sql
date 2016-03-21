-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  name TEXT               NOT NULL,
  id   SERIAL PRIMARY KEY NOT NULL);

-- TOURNAMENT : PAIR UP PLAYERS
CREATE TABLE tournaments (
  name TEXT               NOT NULL,
  id   SERIAL PRIMARY KEY NOT NULL);

-- VIEW FOR PLAYER PARTICULAR TOURNAMENT AND THEIR STATS
CREATE TABLE tournament_players (
  player_id INTEGER REFERENCES players(id)         NOT NULL,
  tournament_id INTEGER REFERENCES tournaments(id) NOT NULL,
  PRIMARY KEY (player_id, tournament_id));

-- VIEW THAT UNIONS players, tournaments and the tournament_players
-- Essentially pulls the text fields so that its both human and machine workable
CREATE VIEW view_players_tournaments AS
  SELECT tournaments.name AS tournament_name,
    tournament_id,
    players.name AS player_name,
    player_id
  FROM tournament_players
  JOIN tournaments ON tournament_id = tournaments.id
  JOIN players ON player_id = players.id;

CREATE VIEW view_tournament_size AS
  SELECT tournament_id, tournament_name, count(tournament_id) AS total_players
  FROM view_players_tournaments
  GROUP BY tournament_id, tournament_name;

CREATE TABLE tournament (
  t_id     INTEGER REFERENCES tournaments(id) NOT NULL,
  player_1 INTEGER REFERENCES players(id),
  player_2 INTEGER REFERENCES players(id),
  winner   INTEGER REFERENCES players(id),
  match    SERIAL                             NOT NULL,
  PRIMARY KEY (t_id, match));

-- TODO: Join tournaments with tournament_players and aggregate on tournament_players and create count(*)
CREATE VIEW tournament_size AS
  SELECT tournament_id, name, count(*) as total_players
  FROM tournament_players
  JOIN tournaments
    ON tournament_id = id
  GROUP BY tournament_id;

CREATE VIEW player_stats AS
  SELECT t_id, count(winner) as games_won, count(*) as matches_played
  FROM tournament