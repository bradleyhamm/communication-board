DROP TABLE IF EXISTS boards;
CREATE TABLE IF NOT EXISTS boards (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL UNIQUE
);

DROP TABLE IF EXISTS images;
CREATE TABLE IF NOT EXISTS images (
    id integer PRIMARY KEY AUTOINCREMENT,
    filename text NOT NULL UNIQUE,
    board_id integer NOT NULL,
    FOREIGN KEY (board_id) REFERENCES boards(id)
);
