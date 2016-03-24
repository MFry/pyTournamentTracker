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
  name  TEXT               NOT NULL,
  match SERIAL             NOT NULL,
  id    SERIAL PRIMARY KEY NOT NULL);

-- View for participants in a particular tournament
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

-- TODO: Figure out why you need to group by multiple group by
CREATE VIEW view_tournament_size AS
  SELECT tournament_id, tournament_name, count(tournament_id) AS total_players
  FROM view_players_tournaments
  GROUP BY tournament_id, tournament_name;

CREATE TABLE tournament_stats (
  t_id     INTEGER REFERENCES tournaments(id)   NOT NULL,
  player   INTEGER REFERENCES players(id)       NOT NULL,
  winner   BOOLEAN                              NOT NULL,
  match    SERIAL REFERENCES tournaments(match) NOT NULL,
  PRIMARY KEY (t_id, match));


INSERT INTO tournaments VALUES('tournament1');
INSERT INTO tournaments VALUES('tournament2');
INSERT INTO players VALUES('p1');
INSERT INTO players VALUES('p2');
INSERT INTO players VALUES('p3');
INSERT INTO players VALUES('p4');
INSERT INTO players VALUES('p5');
INSERT INTO players VALUES('p6');
INSERT INTO tournament_players VALUES(1, 1);
INSERT INTO tournament_players VALUES(2, 1);
INSERT INTO tournament_players VALUES(3, 1);
INSERT INTO tournament_players VALUES(4, 1);
INSERT INTO tournament_players VALUES(5, 2);
INSERT INTO tournament_players VALUES(6, 2);
INSERT INTO tournament_stats VALUES (1, 1, True, 1);
INSERT INTO tournament_stats VALUES (1, 2, False, 1);
INSERT INTO tournament_stats VALUES (2, 5, TRUE, 1);
INSERT INTO tournament_stats VALUES (2, 6, FALSE, 1);
INSERT INTO tournament_stats VALUES (1, 3, TRUE, 2);
INSERT INTO tournament_stats VALUES (1, 4, TRUE, 2);
INSERT INTO tournament_stats VALUES (1, 2, TRUE, 3);
INSERT INTO tournament_stats VALUES (1, 3, FALSE, 3);
INSERT INTO tournament_stats VALUES (1, 4, FALSE, 4);
INSERT INTO tournament_stats VALUES (1, 1, TRUE, 4);
INSERT INTO tournament_stats VALUES (1, 1, TRUE, 5);
INSERT INTO tournament_stats VALUES (1, 3, FALSE, 5);