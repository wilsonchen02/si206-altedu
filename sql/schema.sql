PRAGMA foreign_keys = ON;

CREATE TABLE schools(
    id INTEGER,
    name VARCHAR(128), 
    sat_avg INTEGER,
    grad_rate FLOAT,
    admissions_rate FLOAT,
    size INTEGER,
    zip INTEGER,
    city_id VARCHAR(100),
    UNIQUE(id),
    FOREIGN KEY(city_id) REFERENCES cities(city_id),
    PRIMARY KEY(id)
);

CREATE TABLE cities(
    city_id VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL
);

CREATE TABLE geodb (
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    elevation INTEGER NOT NULL,
    population INTEGER NOT NULL,
    PRIMARY KEY(city)
);