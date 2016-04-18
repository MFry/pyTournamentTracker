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
  name  TEXT   UNIQUE      NOT NULL,
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

-- Stores the matches for each tournament
-- One row per one player that participated in a match in a tournament
CREATE TABLE matches (
  t_id     INTEGER REFERENCES tournaments(id)   NOT NULL,
  player   INTEGER REFERENCES players(id)       NOT NULL,
  winner   BOOLEAN                              NOT NULL,
  match    INTEGER                              NOT NULL,
  PRIMARY KEY (t_id, player, winner, match));

-- Gives stats, games won and games played, for each player in each tournament
CREATE VIEW view_player_stats AS
  SELECT
    view_p_t.tournament_id,
    view_p_t.player_id,
    view_p_t.player_name,
    games_won,
    COALESCE(count(matches.player), 0) AS games_played
  FROM view_players_tournaments AS view_p_t
    LEFT OUTER JOIN matches
      ON view_p_t.tournament_id = matches.t_id
         AND view_p_t.player_id = matches.player
    LEFT OUTER JOIN
    (SELECT
       view_p_t.tournament_id       AS t_id,
       view_p_t.player_id           AS player,
       COALESCE(SUM(CASE WHEN winner
         THEN 1
                    ELSE 0 END), 0) AS games_won
     FROM view_players_tournaments AS view_p_t
       LEFT OUTER JOIN matches
         ON view_p_t.tournament_id = matches.t_id
            AND view_p_t.player_id = matches.player
     GROUP BY view_p_t.tournament_id, view_p_t.player_id) AS player_wins
      ON view_p_t.tournament_id = player_wins.t_id
         AND view_p_t.player_id = player_wins.player
  GROUP BY view_p_t.tournament_id, view_p_t.player_id, view_p_t.player_name, games_won
  ORDER BY view_p_t.tournament_id, games_won DESC, games_played DESC;




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
INSERT INTO tournament_players VALUES(1, 2);
INSERT INTO matches VALUES (1, 1, True, 1);
INSERT INTO matches VALUES (1, 2, False, 1);
INSERT INTO matches VALUES (1, 3, FALSE, 2);
INSERT INTO matches VALUES (1, 4, TRUE, 2);
INSERT INTO matches VALUES (1, 1, TRUE, 3);
INSERT INTO matches VALUES (1, 4, FALSE, 3);
INSERT INTO matches VALUES (1, 2, FALSE, 4);
INSERT INTO matches VALUES (1, 3, TRUE, 4);
-- Nonsensical matches
-- INSERT INTO tournament_stats VALUES (1, 1, FALSE, 5);
-- INSERT INTO tournament_stats VALUES (1, 3, FALSE, 5);
--T2
INSERT INTO matches VALUES (2, 5, TRUE, 1);
INSERT INTO matches VALUES (2, 6, FALSE, 1);
INSERT INTO matches VALUES (2, 1, TRUE, 2);
INSERT INTO matches VALUES (2, 1, TRUE, 3);
INSERT INTO matches VALUES (2, 5, FALSE, 4);

