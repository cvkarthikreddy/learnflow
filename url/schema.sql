CREATE TABLE IF NOT EXISTS url_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_url TEXT UNIQUE NOT NULL,
    long_url TEXT NOT NULL
);