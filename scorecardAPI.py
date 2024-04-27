import requests
import sqlite3

api_key = "YOn4vJlPGcmk32VfxDWB0VvaMDiVNKZ5c1w95CoV"


def api_call():
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
    list = []
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


    for state in us_state_abbreviations:
        base_url = f"http://api.data.gov/ed/collegescorecard/v1/schools?school.state={state}"
        params = {
            "api_key": api_key,
            "fields": f"id,{name},{sat_avg},{grad_rate},{ar},{size},{zip},{city},{state},{lat},{lon}",
            "per_page": 50,
        }
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Print or process your data here
            print(data["results"][0])
        else:
            print("Failed to retrieve data:", response.status_code)
            
def insert_data():
    pass


def main():
    api_call()
    insert_data()
    

if __name__ == '__main__':
    main()