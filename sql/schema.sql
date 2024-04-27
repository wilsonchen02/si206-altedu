PRAGMA foreign_keys = ON;

CREATE TABLE schools(
    id INTEGER NOT NULL,
    name VARCHAR(128) NOT NULL,
    sat_avg INTEGER,
    grad_rate FLOAT,
    admissions_rate FLOAT,
    size INTEGER NOT NULL,
    zip INTEGER,
    city_id INTEGER NOT NULL,
    state_id INTEGER NOT NULL,
    UNIQUE(id),
    PRIMARY KEY(id)
);

-- Includes both states and territories
-- We just won't use the territories
CREATE TABLE states(
    id INTEGER NOT NULL,
    graphql_cursor VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    iso_initials VARCHAR(2) NOT NULL,
    PRIMARY KEY(id)
);

-- This includes city data
CREATE TABLE cities(
    id INTEGER NOT NULL,
    graphql_cursor VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    state_id INTEGER NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    elevation INTEGER NOT NULL,
    population INTEGER NOT NULL,
    UNIQUE(name, state_id),
    PRIMARY KEY(id)
);