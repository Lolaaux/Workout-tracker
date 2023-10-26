import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

basic = HTTPBasicAuth(os.environ["AUTH_USERNAME"], os.environ["AUTH_PASS"])



API_key = os.environ["API_KEY"]
APP_id = os.environ["APP_ID"]
SHEETY_ENDPOINT = "https://api.sheety.co/e03cdb80ea1fa608a98c58d339268d32/workoutTracking/workouts"

GENDER = "Female"
WEIGHT_KG = 60
HEIGHT_CM = 157
AGE = 19

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_id,
    "x-app-key": API_key,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_inputs, auth=basic)
    print(sheet_response.text)

