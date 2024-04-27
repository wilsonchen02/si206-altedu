import requests
import json
import sqlite3

# Fetch data from GeoDB Cities API
# Gets all the states/regions in the US
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
            regions(first: 10) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        isoCode
                        name
                    }
                }
            }
        }
    }
    """

query = """
    query($prev_cursor: String) {
        country(id: "US") {
            regions(first: 10, after: $prev_cursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        isoCode
                        name
                    }
                }
            }
        }
    }
    """

# From hw7
def set_up_database():
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
def geodb_get_states():
    data = {}
    prev_cursor = ""
    hasNextPage = True
    is_first_query = True

    while hasNextPage:
        if is_first_query:
            # Perform first query (try first 10 or less)
            response = requests.post(url=graphql_url, json={"query": first_query}, headers=header)
            is_first_query = False
        else:
            # Not the first query (use prev_cursor as offset for next page)
            variables = {
                "prev_cursor": prev_cursor
            }
            response = requests.post(url=graphql_url, json={"query": query, "variables": variables}, headers=header)
            
        # Check if response is ok
        # If response is ok but GraphQL response isn't, catch it
        if response.status_code == 200:
            data = response.json()
            print("response:", response.content)    # TODO: remove this after done debugging
            
            if data.get("errors") != None:
                print("GraphQL query error")
                return
            
            # TODO: remove this when db is set up
            with open("test_geodb_get_states.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            
            # Check if there's another page available. If so, prepare to get the next one
            hasNextPage = data["data"]["country"]["regions"]["pageInfo"]["hasNextPage"]        
            # Grab value of last city's cursor in the previous batch
            prev_cursor = data["data"]["country"]["regions"]["pageInfo"]["endCursor"]
            
            # Remove duplicates (Los Angeles has 2 entries but different ids, use 2 columns to determine uniqueness)
            # TODO: have this fill up the DB instead of local json (no caching allowed)
            cur, conn = set_up_database()
            
            # Populate states table
            for state in data["data"]["country"]["regions"]["edges"]:
                cur.execute("""
                    INSERT OR IGNORE INTO states (name, iso_initials)
                    VALUES (?, ?)
                    """,
                    (
                        state["node"]["name"],
                        state["node"]["isoCode"]
                    )
                )
                conn.commit()
            
            conn.close()
        else:
            # Response is bad
            print("Failed to retrieve data:", response.status_code)
            return


# TODO: use this to test funcs
def main():
    geodb_get_states()

if __name__ == "__main__":
    main()