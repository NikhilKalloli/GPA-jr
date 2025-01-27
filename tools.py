import datetime
from storage import *
import json
import pytz

import pymongo
import streamlit as st


@st.cache_resource 
def get_database_connection_log():
    client = pymongo.MongoClient(st.secrets["mongo"]["ATLAS_DB_URL"])
    db = client["sgpa-estimator"]
    collection = db["logs"]
    return collection


def grade_estimates(internal_marks):
    grades = ["O", "A+", "A", "B+", "B", "C", "P"]
    grade_values = {}
    for grade in grades:
        if grade == "O":
            grade_values[grade] = [(90 - mark) * 2 if 0 <= (90 - mark) * 2 <= 100 else "" for mark in internal_marks]
        elif grade == "A+":
            grade_values[grade] = [(80 - mark) * 2 if 0 <= (80 - mark) * 2 <= 100 else "" for mark in internal_marks]
        elif grade == "A":
            grade_values[grade] = [(70 - mark) * 2 if 0 <= (70 - mark) * 2 <= 100 else "" for mark in internal_marks]
        elif grade == "B+":
            grade_values[grade] = [(60 - mark) * 2 if 0 <= (60 - mark) * 2 <= 100 else "" for mark in internal_marks]
        elif grade == "B":
            grade_values[grade] = [(55 - mark) * 2 if 0 <= (55 - mark) * 2 <= 100 else "" for mark in internal_marks]
        elif grade == "C":
            grade_values[grade] = [(50 - mark) * 2 if 0 <= (50 - mark) * 2 <= 100 else "" for mark in internal_marks]
        elif grade == "P":
            grade_values[grade] = [(40 - mark) * 2 if 0 <= (40 - mark) * 2 <= 100 else "" for mark in internal_marks]
    return grade_values


def calculate_sgpa(sub_names, sub_creds, grade_lists, grade_in_each):
    # Dictionary mapping grades to grade points
    grade_to_gp = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0}

    # Calculate grade points for each subject
    grade_points = [grade_to_gp[grade] for grade in grade_in_each]

    # Calculate weighted grade points for each subject
    weighted_gp = [gp * creds for gp, creds in zip(grade_points, sub_creds)]

    # Calculate total weighted grade points
    total_weighted_gp = sum(weighted_gp)

    # Calculate total credits
    total_credits = sum(sub_creds)

    # Calculate SGPA
    sgpa = total_weighted_gp / total_credits
    sgpa = round(sgpa, 3)
    return sgpa


def validate_usn(usn):
    # More general pattern
    # pattern = r'^1MS\d{2}[A-Z]{2}\d{3}(-T)?$'

    # Specific to CSE from 001 to 168
    # pattern = r'^1MS22CS(0[0-9][0-9]|1[0-6][0-8])$'

    # For both CSE and ISE
    # pattern = r'^1MS22(CS(0[0-9][0-9]|1[0-6][0-8])|IS(0[0-9][0-9]|1[0-5][0-5]))$'
    if check_usn_exists(usn):
        return True
    return False


def validate_branch(usn, branch_value):

    if usn[5:7] == "CS" and branch_value == "CS":
        return True
    elif usn[5:7] == "IS" and branch_value == "IS":
        return True
    else:
        return False
    

def log_usn_entry(usn, branch_value):
    try:
        # Load subject info
        with open("subject_info.json", "r") as f:
            subject_info = json.load(f)
            branch_dict = {info["Branch"]: info for info in subject_info}

        # Get current timestamp in IST
        ist_tz = pytz.timezone('Asia/Kolkata')  
        timestamp = datetime.datetime.now(ist_tz)

        # Get student name
        name = get_student_name(usn)

        # Get branch name
        branch_name = branch_dict.get(branch_value, {}).get("Branch", "Unknown Branch")

        # Prepare log entry
        log_entry = {
            "timestamp": timestamp,
            "usn": usn,
            "name": name,
            "branch": branch_name
        }

        # Get MongoDB connection
        collection = get_database_connection_log()

        # Insert the log entry
        result = collection.insert_one(log_entry)

        print(f"Log entry written: {log_entry}")
        print(f"MongoDB Document ID: {result.inserted_id}")

    except FileNotFoundError:
        print("Error: subject_info.json not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_logs(limit=None):
    collection = get_database_connection_log()
    logs = collection.find({}).sort("timestamp", -1)
    if limit:
        logs = logs.limit(limit)
    
    # Convert timestamps to IST
    ist_tz = pytz.timezone('Asia/Kolkata')
    converted_logs = []
    for log in logs:
        log['timestamp'] = log['timestamp'].replace(tzinfo=pytz.UTC).astimezone(ist_tz)
        converted_logs.append(log)
    
    return converted_logs


if __name__ == "__main__":
    grade_estimates()
    get_logs()
    get_database_connection_log()
    
