import json
import pandas as pd
import uuid


def generate_uuid(first_name, last_name):
    """Generate a deterministic UUID based on athlete attributes."""
    namespace = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")  # Fixed namespace UUID
    unique_string = f"{first_name.lower()}_{last_name.lower()}"
    return str(uuid.uuid5(namespace, unique_string))

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def coalesce_rows(group: pd.DataFrame) -> pd.Series:
    # For each column in the group, pick the first non-empty value.
    # (Non-empty meaning not NaN and not an empty string.)
    merged = {}
    for col in group.columns:
        non_nulls = group[col].dropna().loc[group[col] != ""]
        if len(non_nulls) > 0:
            merged[col] = non_nulls.iloc[0]
        else:
            merged[col] = ""
    return pd.Series(merged)

def coalesce_df(df: pd.DataFrame, key_col: str) -> pd.DataFrame:
    # Given a dataframe and a column (key_col) that identifies the entity,
    # group by that key and merge partial rows into a single row per key.
    if key_col not in df.columns or df.empty:
        return df
    
    df_coalesced = (
        df.groupby(key_col, as_index=False)
          .apply(coalesce_rows, include_groups=False)
          .reset_index(drop=True)
    )
    return df_coalesced

def json_to_dataframe(data):
    athlete_uuid_map = {}  # Dictionary to track unique athletes
    all_athletes = []
    
    # Catapult
    for athlete in data.get("athletes", []):
        first_name = athlete.get("first_name", "").strip()
        last_name = athlete.get("last_name", "").strip()
        athlete_key = (first_name.lower(), last_name.lower())
        if athlete_key not in athlete_uuid_map:
            athlete_uuid_map[athlete_key] = generate_uuid(first_name, last_name)
        
        all_athletes.append({
            "Athlete UUID": athlete_uuid_map[athlete_key],
            "First Name": first_name,
            "Last Name": last_name,
            "Sex": athlete.get("gender", ""),
            "Home State": athlete.get("home_state", ""),
            "Home Town": athlete.get("home_town", ""),
            "High School": athlete.get("highschool", ""),
            "Date of Birth": athlete.get("date_of_birth_date", ""),
            "Year of Birth": athlete.get("year_of_birth_date", ""),
            "Source": "Catapult",
            "Is Current": True
        })
    
    # ForceDecks
    for athlete in data.get("forcedecks_athletes", []):
        first_name = athlete.get("givenName", "").strip()
        last_name = athlete.get("familyName", "").strip()
        athlete_key = (first_name.lower(), last_name.lower())
        if athlete_key not in athlete_uuid_map:
            athlete_uuid_map[athlete_key] = generate_uuid(first_name, last_name)
        
        all_athletes.append({
            "Athlete UUID": athlete_uuid_map[athlete_key],
            "First Name": first_name,
            "Last Name": last_name,
            "Sex": athlete.get("gender", ""),
            "Home State": athlete.get("home_state", ""),
            "Home Town": "",
            "High School": "",
            "Date of Birth": "",
            "Year of Birth": "",
            "Source": "ForceDecks",
            "Is Current": True
        })
    
    # Build raw df of partial athlete info
    df_athletes_raw = pd.DataFrame(all_athletes)

    dataframes = {}
    
    dataframes["Athletes"] = df_athletes_raw

    dataframes["Teams"] = pd.DataFrame(list({
        athlete["teamId"]: {
            "Team ID": athlete["teamId"],
            "Sport": next(
                (attr["valueName"]
                 for attr in athlete.get("attributes", [])
                 if attr["typeName"] == "Sport"
                ), 
                None
            ),
            "Sex": None,
        }
        for athlete in data.get("forcedecks_athletes", [])
        if "teamId" in athlete
    }.values()))

    # Seasons
    dataframes["Seasons"] = pd.DataFrame([
        {
            "Season ID": period["id"],
            "Season year": period["name"],
            "Sport": None
        }
        for period in data.get("periods", [])
    ])

    # Athlete Seasons
    dataframes["Athlete Seasons"] = pd.DataFrame([
        {
            "Athlete Season id": None,
            "Athlete UUID": athlete["id"],
            "Season ID": None,  # Needs mapping
            "Team ID": athlete.get("current_team_id", "")
        }
        for athlete in data.get("athletes", [])
    ])

    # Events
    dataframes["Events"] = pd.DataFrame([
        {
            "Event ID": period["id"],
            "Team ID": None,
            "Event Type": period["name"],
            "Start Unix": period["start_time"],
            "End Unix": period["end_time"],
            "Team Result": None
        }
        for period in data.get("periods", [])
    ])

    # Performances
    dataframes["Performances"] = pd.DataFrame([
        {
            "Performance ID": activity["id"],
            "Event ID": None,  # Needs mapping
            "Athlete UUID": None,  # Needs mapping
            "Athlete opponent": None,
            "Team ID": activity.get("owner_id", ""),
            "Start Unix": activity["start_time"],
            "End Unix": activity["end_time"],
            "Result": None,  # Placeholder for sensor data
        }
        for activity in data.get("activities", [])
    ])

    # Performance Results
    dataframes["Performance Results"] = pd.DataFrame([
        {
            "Performance Result ID": activity["id"],
            "Performance ID": None,  # Needs mapping
            "Modality ID": None,     # Needs mapping
            "Result": None,          # Placeholder for sensor data
            "Is Raw": True
        }
        for activity in data.get("activities", [])
    ])

    # Tests
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

    # Test Results
    dataframes["Test Results"] = pd.DataFrame([
        {
            "Test Result ID": f"{test['id']}-{result['resultId']}",
            "Test ID": test["id"],
            "Result": result["value"],
            "Is Raw": True
        }
        for test in data.get("forcedecks_tests", [])
        for result in test["results"]
    ])

    # Modalities
    dataframes["Modalities"] = pd.DataFrame()

    # Athlete Metadata
    dataframes["Athlete Metadata"] = pd.DataFrame([
        {
            "Athlete UUID": athlete["id"],
            "Sex": athlete.get("gender", ""),
            "Jersey": athlete.get("jersey", ""),
            "Velocity Max": athlete.get("velocity_max", None),
            "Acceleration Max": athlete.get("acceleration_max", None),
            "Heart Rate Max": athlete.get("heart_rate_max", None),
            "Player Load Max": athlete.get("player_load_max", None),
            "Weight": athlete.get("weight", None),
            "Height": athlete.get("height", None),
            "Age": athlete.get("age", None),
            "Team ID": athlete.get("current_team_id", ""),
            "Position": athlete.get("position_name", ""),
            "Is Current": True
        }
        for athlete in data.get("athletes", [])
    ])

    # Medical
    dataframes["Medical"] = pd.DataFrame([
        {
            "Medical Record ID": record["id"],
            "Athlete UUID": record["athlete_uuid"],
            "Date": record["date"],
            "Record": record["record"]
        }
        for record in data.get("medical_records", [])
    ])

    # Academic Records
    dataframes["Academic Records"] = pd.DataFrame([
        {
            "Academic Record ID": record["id"],
            "Athlete UUID": record["athlete_uuid"],
            "Date": record["date"],
            "Record": record["record"]
        }
        for record in data.get("academic_records", [])
    ])

    # Consent
    dataframes["Consent"] = pd.DataFrame([
        {
            "Record ID": record["id"],
            "Athlete UUID": record["athlete_uuid"],
            "Consent Status": record["consent_status"]
        }
        for record in data.get("consent", [])
    ])

#This is the list of the dataframes to bring togehter to make one entry per UUID or Team ID etc
    coalesce_map = {
        "Athletes": "Athlete UUID",
        "Teams": "Team ID",
        "Seasons": "Season ID",
        "Athlete Seasons": "Athlete Season id",
        "Events": "Event ID",
        "Performances": "Performance ID",
        "Performance Results": "Performance Result ID",
        "Tests": "Test ID",
        "Test Results": "Test Result ID",
        "Athlete Metadata": "Athlete UUID",
        "Medical": "Medical Record ID",
        "Academic Records": "Academic Record ID",
        "Consent": "Record ID"
        # "Modalities": <whatever ID column you need, if any>
    }
    
    for df_name, df_obj in dataframes.items():
        key_col = coalesce_map.get(df_name)
        if key_col:  # Only coalesce if we have a mapping
            dataframes[df_name] = coalesce_df(df_obj, key_col)
    
    return dataframes

def export_to_json(dataframes, output_path):
    formatted_output = {key: df.to_dict(orient="records") for key, df in dataframes.items()}
    with open(output_path, "w") as outfile:
        json.dump(formatted_output, outfile, indent=4)
    print(f"Data exported to {output_path}")


# Load your data
input_json_files = {
    "athletes": "Catapult/athletes.json",
    "forcedecks_athletes": "ForceDecks/ForceDecks/forcedecks_athletes.json",
    "forcedecks_tests": "ForceDecks/ForceDecks/forcedecks_tests.json",
    "periods": "Catapult/periods.json",
    "activities": "Catapult/activities.json"
}

data = {key: load_json(path) for key, path in input_json_files.items()}

# Convert to dataframes and coalesce
dataframes = json_to_dataframe(data)

# Export
output_json_path = "formatted_output.json"
export_to_json(dataframes, output_json_path)

# Check results
for name, df in dataframes.items():
    print(f"--- {name} ---")
    display(df)
