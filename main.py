
# Nutritionix Natural Language for Exercise api documentation:
# https://developer.syndigo.com/docs/natural-language-for-exercise
# Currently the documentation is incomplete. The Parameters section
# does not contain any info (2023-12-6)
# Sheety is used to interact with Google Sheets: https://sheety.co/

# Pycharm could not install dotenv. Run this command from the terminal.
# pip install python-dotenv
from dotenv import load_dotenv
import os
import requests
import datetime as dt


load_dotenv(".env")
NUTRITIONIX_NATURAL_LANGUAGE_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITIONIX_HEADERS = {
    "x-app-id": os.environ['NUTRITIONIX_APP_ID'],
    "x-app-key": os.environ['NUTRITIONIX_APP_KEY'],
    "x-remote-user-id": "0"
}

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
SHEETY_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['SHEETY_TOKEN']}"
}


def request_exercise_data(user_text):

    nutritionix_json = {
        "query": user_text
    }

    response = requests.post(
        url=NUTRITIONIX_NATURAL_LANGUAGE_EXERCISE_ENDPOINT,
        headers=NUTRITIONIX_HEADERS,
        json=nutritionix_json
    )

    response.raise_for_status()
    return response.json()["exercises"]


def add_data_to_google_sheet(exercises):

    now = dt.datetime.now()
    today = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M:%S")

    for exercise in exercises:
        sheety_json = {
            "workout": {
                "date": today,
                "time": time,
                "exercise": str(exercise['name']).title(),
                "duration": exercise['duration_min'],
                "calories": exercise['nf_calories']
            }
        }

        response = requests.post(url=SHEETY_ENDPOINT, headers=SHEETY_HEADERS, json=sheety_json)
        print(response.status_code)
        print(response.text)


user_input = input("Tell me which exercises you did:\n")
exercise_data = request_exercise_data(user_text=user_input)
add_data_to_google_sheet(exercises=exercise_data)
