--
-- Table definitions for the tournament project.
--

-- If you want to clear the database uncomment the line below
-- DROP DATABASE IF EXISTS tournament;
CREATE DATABASE IF NOT EXISTS tournament;

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
  tournament_id INTEGER REFERENCES tournaments (id)           NOT NULL,
  player        INTEGER REFERENCES players (id)               NOT NULL,
  winner        BOOLEAN                                       NOT NULL,
  match         INTEGER                                       NOT NULL,
  PRIMARY KEY (tournament_id, player, winner, match)
);

-- Gives stats, games won and games played, for each player in each tournament
CREATE VIEW view_player_stats AS
  SELECT
    view_p_t.tournament_id             AS t_id,
    view_p_t.player_id                 AS p_id,
    view_p_t.player_name,
    games_won,
    COALESCE(count(matches.player), 0) AS games_played
  FROM view_players_tournaments AS view_p_t
    LEFT OUTER JOIN matches
      ON view_p_t.tournament_id = matches.tournament_id
         AND view_p_t.player_id = matches.player
    LEFT OUTER JOIN
    (SELECT
       view_p_t.tournament_id       AS t_id,
       view_p_t.player_id           AS player,
       COALESCE(SUM(CASE WHEN winner
         THEN 1 ELSE 0 END), 0) AS games_won
     FROM view_players_tournaments AS view_p_t
       LEFT OUTER JOIN matches
         ON view_p_t.tournament_id = matches.tournament_id
            AND view_p_t.player_id = matches.player
     GROUP BY view_p_t.tournament_id, view_p_t.player_id) AS player_wins
      ON view_p_t.tournament_id = player_wins.t_id
         AND view_p_t.player_id = player_wins.player
  GROUP BY view_p_t.tournament_id, view_p_t.player_id, view_p_t.player_name, games_won
  ORDER BY view_p_t.tournament_id, games_won DESC, games_played DESC;



