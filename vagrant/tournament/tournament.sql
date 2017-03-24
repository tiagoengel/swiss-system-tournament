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

CREATE TABLE matches ( player INTEGER REFERENCES players(id),
                       opponent INTEGER REFERENCES players(id),
                       won INTEGER,
                       points INTEGER DEFAULT 0 );


CREATE VIEW player_status as
  SELECT players.id,
         players.name,
         coalesce(sum(matches.won), 0) as wins,
         count(matches.won) as matches,
         coalesce(sum(matches.points), 0) as points
  FROM players
  LEFT JOIN matches on players.id = matches.player
  GROUP BY players.id
  ORDER BY wins, points;


