import requests

api_key = "YOn4vJlPGcmk32VfxDWB0VvaMDiVNKZ5c1w95CoV"

base_url = "http://api.data.gov/ed/collegescorecard/v1/schools"

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


params = {
    "api_key": api_key,
    "fields": f"id,{name},{sat_avg},{grad_rate},{ar},{size},{zip},{city},{state},{lat},{lon}",
    "per_page": 1,
}

# Make a GET request
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Print or process your data here
    print(data)
else:
    print("Failed to retrieve data:", response.status_code)
