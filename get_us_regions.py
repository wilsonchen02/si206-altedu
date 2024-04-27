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
                    cursor
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
                    cursor
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
def geodb_get_states():
    data = {}
    # Check db to see if there's anything to start with
    # Otherwise, start at the beginning
    prev_cursor = check_cursor()
    hasNextPage = True

    # On each result page, check if the data is already in the db
    # If it is, grab the next page if possible and try again
    # Otherwise, add new data from page into db
    while hasNextPage:
        # If there's nothing in the table, start at the beginning
        # Else, start from the last one in the table
        # print(f"start of while loop, prev_cursor: {prev_cursor}")
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
            with open("test_geodb_get_states.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            
            # Check if there's another page available. If so, prepare to get the next one
            hasNextPage = data["data"]["country"]["regions"]["pageInfo"]["hasNextPage"]        
            # Grab value of last city's cursor in the previous batch
            prev_cursor = data["data"]["country"]["regions"]["pageInfo"]["endCursor"]
            
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
        SELECT graphql_cursor FROM states
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
    if len(data["data"]["country"]["regions"]["edges"]) == 0:
        return None
    
    first_state_name = data["data"]["country"]["regions"]["edges"][0]["node"]["name"]
    print(first_state_name)
    cur.execute("""
        SELECT COUNT(*) FROM states
        WHERE name = ?
        """,
        (first_state_name,)
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
def update_db(data):
    cur, conn = connect_to_db()
    
    # Populate states table
    for state in data["data"]["country"]["regions"]["edges"]:
        cur.execute("""
            INSERT OR IGNORE INTO states (graphql_cursor, name, iso_initials)
            VALUES (?, ?, ?)
            """,
            (
                state["cursor"],
                state["node"]["name"],
                state["node"]["isoCode"]
            )
        )
        conn.commit()
    
    conn.close()


# TODO: use this to test funcs
def main():
    geodb_get_states()

if __name__ == "__main__":
    main()