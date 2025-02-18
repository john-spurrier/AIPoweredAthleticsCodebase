import json
import pandas as pd

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def json_to_dataframe(data):
    dataframes = {}
    
    dataframes["Athletes"] = pd.DataFrame([
        {
            "Athlete UUID": athlete["id"],
            "First Name": athlete.get("first_name", ""),
            "Last Name": athlete.get("last_name", ""),
            "Sex": athlete.get("gender", ""),
            "Home State": athlete.get("home_state", ""),
            "Home Town: ": athlete.get("home_town", ""),
            "High School: ": athlete.get("highschool", ""),
            "Jersey": athlete.get("jersey", ""),
            "Date of Birth": athlete.get("date_of_birth_date", ""),
            "Year of Birth": athlete.get("year_of_birth_date", ""),
            "Velocity Max": athlete.get("velocity_max", None),
            "Acceleration Max": athlete.get("acceleration_max", None),
            "Heart Rate Max": athlete.get("heart_rate_max", None),
            "Player Load Max": athlete.get("player_load_max", None),
            "Team ID": athlete.get("current_team_id", ""),
            "Position": athlete.get("position_name", ""),
            "Is Current": True
        }
        for athlete in data.get("athletes", [])
    ])
    
    dataframes["Teams"] = pd.DataFrame(list({
        athlete["teamId"]: {
            "Team ID": athlete["teamId"],
            "Sport": next((attr["valueName"] for attr in athlete.get("attributes", []) if attr["typeName"] == "Sport"), None),
            "Sex": None,
            "Season": None
        }
        for athlete in data.get("forcedecks_athletes", [])
    }.values()))
    
    dataframes["Events"] = pd.DataFrame([
        {
            "Event ID": period["id"],
            "Team ID": None,
            "Event Type": period["name"],
            "Team Opponent": None,
            "Start Unix": period["start_time"],
            "End Unix": period["end_time"],
            "Team Result": None
        }
        for period in data.get("periods", [])
    ])
    
    dataframes["Performances"] = pd.DataFrame([
        {
            "Performance ID": activity["id"],
            "Event ID": None,  # Needs mapping
            "Athlete UUID": None,  # Needs mapping
            "Team ID": activity.get("owner_id", ""),
            "Start Unix": activity["start_time"],
            "End Unix": activity["end_time"]
        }
        for activity in data.get("activities", [])
    ])
    
    dataframes["Performance Results"] = pd.DataFrame([
        {
            "Performance Result ID": activity["id"],
            "Performance ID": None,  # Needs mapping
            "Athlete UUID": None,  # Needs mapping
            "Team ID": activity.get("owner_id", ""),
            "Modality ID": None,  # Needs mapping
            "Result": None,  # Placeholder for sensor data
            "Is Raw": True
        }
        for activity in data.get("activities", [])
    ])
    
    dataframes["Tests"] = pd.DataFrame([
        {
            "Test ID": test["id"],
            "Athlete UUID": test["athleteId"],
            "Team ID": None,
            "Modality ID": None,
            "Start Unix": test["startTime"],
            "End Unix": test["endTime"],
            "Date Uploaded": test["recordedUTC"],
            "Test Type": None
        }
        for test in data.get("forcedecks_tests", [])
    ])
    
    dataframes["Test Results"] = pd.DataFrame([
        {
            "Test Result ID": f"{test['id']}-{result['resultId']}",
            "Test ID": test["id"],
            "Athlete UUID": test["athleteId"],
            "Team ID": None,
            "Modality ID": None,
            "Result": result["value"],
            "Is Raw": True
        }
        for test in data.get("forcedecks_tests", []) for result in test["results"]
    ])

    dataframes["Modalities"] = pd.DataFrame()
    dataframes["Athlete Metadata"] = pd.DataFrame()
    
    return dataframes

def export_to_json(dataframes, output_path):
    formatted_output = {key: df.to_dict(orient="records") for key, df in dataframes.items()}
    
    with open(output_path, "w") as outfile:
        json.dump(formatted_output, outfile, indent=4)
    print(f"Data exported to {output_path}")

input_json_files = {
    "athletes": "Catapult/athletes.json",
    "forcedecks_athletes": "ForceDecks/ForceDecks/forcedecks_athletes.json",
    "forcedecks_tests": "ForceDecks/ForceDecks/forcedecks_tests.json",
    "periods": "Catapult/periods.json",
    "activities": "Catapult/activities.json"
}

data = {key: load_json(path) for key, path in input_json_files.items()}
dataframes = json_to_dataframe(data)
output_json_path = "formatted_output.json"
export_to_json(dataframes, output_json_path)


for name, df in dataframes.items():
    print(f"--- {name} ---")
    display(df) 