CREATE TABLE users
(
    id       integer PRIMARY KEY,
    user     VARCHAR UNIQUE NOT NULL,
    email    VARCHAR UNIQUE,
    password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user'
);

CREATE TABLE playlist
(
    id     integer PRIMARY KEY,
    name   VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    album  VARCHAR NOT NULL,
    genre  VARCHAR NOT NULL,
    user_id INT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO playlist ("name", "artist", "album", "genre")
VALUES ('Shape of You', 'Ed Sheeran', 'Divide', 'Pop'),
       ('Blinding Lights', 'The Weeknd', 'After Hours', 'R&B'),
       ('Bohemian Rhapsody', 'Queen', 'A Night at the Opera', 'Rock'),
       ('Smells Like Teen Spirit', 'Nirvana', 'Nevermind', 'Grunge'),
       ('Levitating', 'Dua Lipa', 'Future Nostalgia', 'Pop');



