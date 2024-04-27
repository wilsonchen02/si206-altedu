import requests
import json
import os
import sqlite3

# Fetch data from GeoDB Cities API
# Particularly [name, lat, long, elevation, population, region]
# of cities in the US
# NOTE: the free API limits to 10 results per request
# NOTE: trying to fetch an amount N > max results will return max results

# This uses a public API key
# base_url = "http://geodb-free-service.wirefreethought.com/v1/geo/"
graphql_url = "http://geodb-free-service.wirefreethought.com/graphql"

header = {
    "content-type": "application/json"
}

first_query = """
    query {
        country(id: "US") {
            name
            populatedPlaces(types: ["CITY"], first: 10) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    cursor
                    node {
                        name
                        latitude
                        longitude
                        elevationMeters
                        population
                        region {
                            name
                        }
                    }
                }
            }
        }
    }
    """

query = """
    query($prev_cursor: String) {
        country(id: "US") {
            name
            populatedPlaces(types: ["CITY"], first: 10, after: $prev_cursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    cursor
                    node {
                        name
                        latitude
                        longitude
                        elevationMeters
                        population
                        region {
                            name
                        }
                    }
                }
            }
        }
    }
    """

# From hw7
def connect_to_db():
    """
    Sets up a SQLite database connection and cursor.

    Parameters
    -----------------------
    db_name: str
        The name of the SQLite database.

    Returns
    -----------------------
    Tuple (Cursor, Connection):
        A tuple containing the database cursor and connection objects.
    """
    conn = sqlite3.connect("var/database.sqlite")
    cur = conn.cursor()
    return cur, conn

# TODO: first req should not have the "after" parameter for populatedPlaces
# Use GraphQL pagination to get the next 10 cities
# Running this function will place 20 entries at a time into the db
def geodb_get_cities():
    data = {}
    prev_cursor = check_cursor()
    hasNextPage = True

    while hasNextPage:
        if prev_cursor != None:
            variables = {
                "prev_cursor": prev_cursor
            }
            response = requests.post(url=graphql_url, json={"query": query, "variables": variables}, headers=header)
        else:
            # Perform first query (try first 10 or less)
            response = requests.post(url=graphql_url, json={"query": first_query}, headers=header)
            
        # Check if response is ok
        # If response is ok but GraphQL response isn't, catch it
        if response.status_code == 200:
            data = response.json()
            # print("response:", response.content)    # TODO: remove this after done debugging
            
            if data.get("errors") != None:
                print("GraphQL query error")
                return
            
            # TODO: remove this when db is set up
            with open("test_geodb_get_cities.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            
            # Check if there's another page available. If so, prepare to get the next one
            hasNextPage = data["data"]["country"]["populatedPlaces"]["pageInfo"]["hasNextPage"]        
            # Grab value of last city's cursor in the previous batch
            prev_cursor = data["data"]["country"]["populatedPlaces"]["pageInfo"]["endCursor"]
            
            # Check if this page of data exists in the db
            in_db = check_in_db(data)
            if in_db == False:
                # Update the db
                update_db(data)
                return
            elif in_db == None:
                # No more data left to obtain
                print("No more data left to read")
                return
            
        else:
            # Response is bad
            print("Failed to retrieve data:", response.status_code)
            return

# Check for last used cursor
def check_cursor():
    cur, conn = connect_to_db()
    # Get the cursor of the last record
    cur.execute("""
        SELECT graphql_cursor FROM cities
        ORDER BY id DESC LIMIT 1
        """
    )
    
    # Should return a cursor (or None if table is empty)
    prev_cursor = cur.fetchone()
    conn.close()
    
    # print(f"previous cursor: {prev_cursor}")
    
    if prev_cursor != None:
        return prev_cursor[0]
    else:
        return None

# Check if data from this page already exists in db
def check_in_db(data):
    cur, conn = connect_to_db()
    
    # No more after this node, return
    if len(data["data"]["country"]["populatedPlaces"]["edges"]) == 0:
        return None
    
    first_city_cursor = data["data"]["country"]["populatedPlaces"]["edges"][0]["cursor"]
    print(first_city_cursor)
    cur.execute("""
        SELECT COUNT(*) FROM cities
        WHERE graphql_cursor = ?
        """,
        (first_city_cursor,)
    )
    
    # Should return count (0 or nonzero)
    in_db = cur.fetchone()[0]
    conn.close()
    
    # If exists, return true. Else, return false
    if in_db == 0:
        return False
    else:
        return True

# Fill up the DB instead with the new page of results
# TODO: Remove duplicates (Los Angeles has 2 entries but different ids, use 2 columns to determine uniqueness)
def update_db(data):
    cur, conn = connect_to_db()
    
    # Populate states table
    for city in data["data"]["country"]["populatedPlaces"]["edges"]:
        cur.execute("""
            INSERT OR IGNORE INTO cities (graphql_cursor, name, state_id, latitude, longitude, elevation, population)
            VALUES (?, ?,
            (
                SELECT id FROM states
                WHERE name = ?
            ),
            ?, ?, ?, ?)
            """,
            (
                city["cursor"],
                city["node"]["name"],
                city["node"]["region"]["name"],
                city["node"]["latitude"],
                city["node"]["longitude"],
                city["node"]["elevationMeters"],
                city["node"]["population"]
            )
        )
        conn.commit()
    
    conn.close()

# TODO: use this to test funcs
def main():
    geodb_get_cities()

if __name__ == "__main__":
    main()