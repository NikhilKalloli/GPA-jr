import datetime
import json

def log_usn_entry(usn, branch_value):
    try:
        with open("subject_info.json", "r") as f:
            subject_info = json.load(f)
            branch_dict = {info["Branch"]: info for info in subject_info}

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        branch_name = branch_dict.get(branch_value, {}).get("Branch", "Unknown Branch")

        log_entry = f"{timestamp} | USN: {usn} | Branch: {branch_name}"

        with open("./data/logs.log", "a") as log_file:
            log_file.write(log_entry + "\n")

        print(f"Log entry written: {log_entry}")

    except FileNotFoundError:
        print("Error: subject_info.json not found.")
    except Exception as e:
        print(f"Error: {str(e)}")
