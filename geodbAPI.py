import requests
import json

# Fetch data from GeoDB Cities API
# Particularly [name, lat, long, elevation, population, region]
# of cities in the US
# NOTE: the free API limits to 10 results per request

# This uses a public API key
# base_url = "http://geodb-free-service.wirefreethought.com/v1/geo/"
graphql_url = "http://geodb-free-service.wirefreethought.com/graphql"

header = {
    "content-type": "application/json"
}

query = """
query {
    country(id:"US") {
        name
        populatedPlaces {
            totalCount
            edges {
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

response = requests.post(url=graphql_url, json={"query": query}, headers=header)
print("response status code: ", response.status_code)

if response.status_code == 200: 
    data = response.json()
    print("response: ", response.content)
else:
    print("Failed to retrieve data:", response.status_code)
    
# TODO: have this fill up the DB instead of local json (no caching allowed)
with open("test_geodb_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

# Fetch data from API and store into db
# Can only 
def geodb_update():
    pass
    # Obtain all city IDs in the US (cities?countryIds=US)
    
    
    # Obtain elevation of places (geo/places)
    

# Fetch stored data from db


# TODO: use this to test funcs
def main():
    # geodb_update()
    pass


if __name__ == "__main__":
    main()