import requests
import sqlite3
import os
import sys

api_key = "YOn4vJlPGcmk32VfxDWB0VvaMDiVNKZ5c1w95CoV"


def convert_state_id(state):
    state_dict = {
        "AL" : 0,
        "AK": 1,
        "AZ": 2,
        "AR": 3,
        "CA": 4,
        "CO": 5,
        "CT": 6,
        "DE": 7,
        "FL": 8,
        "GA": 9,
        "HI": 10,
        "ID": 11,
        "IL": 12,
        "IN": 13,
        "IA": 14,
        "KS": 15,
        "KY": 16,
        "LA": 17,
        "ME": 18,
        "MD": 19,
        "MA": 20,
        "MI": 21,
        "MN": 22,
        "MS": 23,
        "MO": 24,
        "MT": 25,
        "NE": 26,
        "NV": 27,
        "NH": 28,
        "NJ": 29,
        "NM": 30,
        "NY": 31,
        "NC": 32,
        "ND": 33,
        "OH": 34,
        "OK": 35,
        "OR": 36,
        "PA": 37,
        "RI": 38,
        "SC": 39,
        "SD": 40,
        "TN": 41,
        "TX": 42,
        "UT": 43,
        "VT": 44,
        "VA": 45,
        "WA": 46,
        "WV": 47,
        "WI": 48,
        "WY": 49,
    }
    if state not in state_dict:
        exit(1)
    return state_dict[state]

def check_state(input):
    us_state_abbreviations = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]
    if input in us_state_abbreviations:
        return True
    else:
        return False

def api_call(state_in):
    name = "school.name"
    sat_avg = "latest.admissions.sat_scores.average"
    grad_rate = "latest.completion.completion_rate_4yr_100nt"
    ar = "latest.admissions.admission_rate.overall"
    size = "latest.student.size"
    zip = "latest.school.zip"
    city = "latest.school.city"
    state = "latest.school.state"
    lat = "location.lat"
    lon = "location.lon"

    base_url = f"http://api.data.gov/ed/collegescorecard/v1/schools?school.state={state_in}&latest.student.size__range=4000.."
    params = {
        "api_key": api_key,
        "fields": f"id,{name},{sat_avg},{grad_rate},{ar},{size},{zip},{city},{state},{lat},{lon}",
        "per_page": 25,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        exit(1)

def db_setup():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(f"{path}/var/database.sqlite")
    cur = conn.cursor()
    return cur, conn

def insert_data(cur, conn, data):
    for d in data:
        cur.execute(
            """
            INSERT OR IGNORE INTO schools (id, name, sat_avg, grad_rate, admissions_rate, size, zip, city_id) VALUES(?,?,?,?,?,?,?,?)    
            """,
            (
                int(d["id"]),
                d["school.name"],
                d["latest.admissions.sat_scores.average.overall"],
                d["latest.completion.completion_rate_4yr_100nt"],
                d["latest.admissions.admission_rate.overall"],
                d["latest.student.size"],
                d["latest.school.zip"],
                d["latest.school.city"],
            ),
        )
    conn.commit()


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("Input a state abbreviation as an argument")
        exit(1)

    state = args[0]
    if not check_state(state):
        print("Enter a valid state")
        exit(1)

    data = api_call(state)
    # print(data["results"])
    
    cur, conn = db_setup()
    insert_data(cur, conn, data["results"])


if __name__ == "__main__":
    main()
