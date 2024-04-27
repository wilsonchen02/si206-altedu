PRAGMA foreign_keys = ON;

CREATE TABLE schools(
    id INTEGER NOT NULL,
    name VARCHAR(128) NOT NULL, 
    sat_avg INTEGER NOT NULL,
    grad_rate FLOAT NOT NULL,
    admissions_rate FLOAT NOT NULL,
    size INTEGER NOT NULL,
    zip INTEGER NOT NULL,
    city_id VARCHAR(100) NOT NULL,
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