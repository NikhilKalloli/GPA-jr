import streamlit as st
from common import *
from tools import *
from storage import *
from upload import *
import json


st.set_page_config(page_title="Admin Panel", page_icon="👨‍💻", layout="centered")

local_css("styles.css")
local_html("index.html")

st.title("Admin Panel")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["Admin"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


def admin_panel():
    """Displays admin panel with options for managing user data."""

    if not check_password():
        st.stop()

    st.subheader("Manage User Data")

    if st.button("Delete All"):
        radio = st.radio("Are you sure?", ("No","Yes"))
        if radio == "Yes":
            if delete_all():
                st.success("All users' data deleted successfully!")

    if st.button("Delete one"):
        usn = st.text_input("Enter USN")
        semester = st.number_input("Enter Semester", min_value=1, max_value=8)
        
        radio = st.radio("Are you sure?", ("No","Yes"))
        if radio == "Yes":
            if check_usn_exists(usn):
                if delete_student_data(usn, semester):
                    st.success(f"{usn} deleted successfully!")

    if st.button("Add all"):
        if insert_CSE() and insert_ISE():
            st.success("All users added with default values successfully!")

    if st.button("Add Specific User"):
        # Logic to add a specific user
        usn = st.text_input("Enter USN").upper()
        name = st.text_input("Enter Name")
        semester = st.number_input("Enter Semester", min_value=4, max_value=8)

        branch_mapping = {"CSE": "CS", "ISE": "IS"}
        branch = st.selectbox("Select Branch", list(branch_mapping.keys()))
        branch_value = branch_mapping[branch]

        with open("subject_info.json", "r") as f:
            subject_info = json.load(f)

        branch_subjects = next((item["Subjects"] for item in subject_info if item["Branch"] == branch_value), None)
        if branch_subjects:
            sub_names = [subject["SubjectName"] for subject in branch_subjects]
            internal_marks = {subject: 0 for subject in sub_names}
        else:
            st.error(f"No subject information found for branch {branch}")

        if branch_subjects:
            if branch_value == "CS" and insert_student_data(usn, name, semester, branch_value, internal_marks):
                st.success("Specific user added successfully!")
            elif branch_value == "IS" and insert_student_data(usn, name, semester, branch_value, internal_marks):
                st.success("Specific user added successfully!")
        else:
            st.error("Failed to add specific user due to missing subject information.")


    if st.button("logs"):

        logs = get_logs(limit=30)
        st.header("Recent Logs")

        for log in logs:
            ist_time = log['timestamp'].strftime("%Y-%m-%d %H:%M:%S %Z")
            st.write(f"{ist_time} | USN: {log['usn']} | Name: {log['name']} | Branch: {log['branch']}")

# if usn of branch change students is still with old branch then they can't login beacuse their usn: 1MS22ME001 but branch CSE.
#  They'll be in Database but they can't login beacuse of validate_branch function in Home.py
# If they have have new usn then they can login.


        

if __name__ == "__main__":
    admin_panel()