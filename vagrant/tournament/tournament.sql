-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\connect tournament;

CREATE TABLE players ( id serial PRIMARY KEY,
                       name TEXT NOT NULL );

CREATE TABLE tournaments ( id serial PRIMARY KEY,
                           name TEXT NOT NULL );

CREATE TABLE tournament_players ( tournament INTEGER REFERENCES tournaments(id),
                                  player INTEGER REFERENCES players(id) );

CREATE TABLE matches ( tournament INTEGER REFERENCES tournaments(id),
                       player INTEGER REFERENCES players(id),
                       opponent INTEGER REFERENCES players(id),
                       won INTEGER,
                       points INTEGER DEFAULT 0 );


CREATE VIEW tournament_status as
  SELECT tournaments.id,
         tournaments.name,
         players.id as player_id,
         players.name as player_name,
         coalesce(sum(matches.won), 0) as wins,
         count(matches.won) as matches,
         coalesce(sum(matches.points), 0) as points
  FROM tournaments
  JOIN tournament_players
    ON tournaments.id = tournament_players.tournament
  JOIN players
    ON tournament_players.player = players.id
  LEFT JOIN matches
    ON tournaments.id = matches.tournament
   AND players.id = matches.player
  GROUP BY tournaments.id, players.id
  ORDER BY tournaments.id, wins desc, points desc, players.id;


