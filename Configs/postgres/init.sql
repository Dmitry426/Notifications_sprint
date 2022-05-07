-- schema.sql
-- Since we might run the import many times we'll drop if exists
DROP DATABASE IF EXISTS data;

CREATE DATABASE data;

\c data;


CREATE TABLE IF NOT EXISTS user_loh (
  id SERIAL PRIMARY KEY,
  username VARCHAR,
  email VARCHAR
);


CREATE TABLE IF NOT EXISTS post (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES user_loh(id),
  title VARCHAR,
  content TEXT,
  image VARCHAR,
  date DATE DEFAULT CURRENT_DATE
);
