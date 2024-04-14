import json

with open("test.json", "r") as file:
    data = json.loads(file.read())

sat_scores_avg = data["results"][0]["latest"]["admissions"]["sat_scores"]["average"]
graduation_rate_4yrs = data["results"][0]["latest"]["completion"][
    "completion_rate_4yr_100nt"
]
admissions_rate = data["results"][0]["latest"]["admissions"]["admission_rate"]["overall"]
size = data["results"][0]["latest"]["student"]["size"]
zip = data["results"][0]["latest"]["school"]["zip"]
city = data["results"][0]["latest"]["school"]["city"]
state = data["results"][0]["latest"]["school"]["state"]
latitude = data["results"][0]["location"]["lat"]
longitude = data["results"][0]["location"]["lon"]



