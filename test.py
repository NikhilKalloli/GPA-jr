import streamlit as st
import pandas as pd
from common import *
import json
from tools import *
from storage import *



st.set_page_config(page_title="Calculla - GPA Calculator", page_icon="📊", layout="centered")
local_css("styles.css")
local_html("index.html")

st.title("Calculla - GPA Calculator")
grade_to_gp = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0}
tab1, tab2, tab3, tab4 = st.tabs(["Details", "CIE - Marks", "Grades - Score", "Credit - GPA"])


def tab_1():
    st.subheader("Enter Details")
    usn = st.text_input("Enter Valid USN", placeholder="1ms22cs000").strip().upper()
    if usn != "" and not validate_usn(usn):
        st.error("Please enter a valid USN")  
        st.stop()  
    # semester = st.selectbox("Select Semester", ["1", "2", "3", "4", "5", "6", "7", "8"])
    # branch = st.selectbox("Select Branch", ["CSE", "ISE", "CSE (AIML)","CSE(CY)", "AIDS", "AIML","ECE", "EEE","ETE","EIE","MECH", "CIVL", "MLE", 
    # "CH","BT","IEM"])
    semester = st.selectbox("Select Semester", ["4"])

    branch_mapping = {"CSE": "CS", "ISE": "IS"}
    branch = st.selectbox("Select Branch", list(branch_mapping.keys()))
    branch_value = branch_mapping[branch]

    if usn!="" and not validate_branch(usn, branch_value):
        st.error("Please enter a valid USN for the selected branch")
        st.stop()

    return usn, semester, branch_value


internal_marks = {}  # Initialize an empty dictionary for internal_marks

def tab_2(usn, semester, branch_value):
    st.subheader("Enter Internal Marks")
    if not validate_usn(usn):
        st.error("Please enter a valid USN")
        st.stop()

    # Load subject information from the JSON file
    with open("subject_info.json", "r") as f:
        subject_info = json.load(f)

    branch_info = next((b for b in subject_info if b["Branch"] == branch_value), None)
    if not branch_info:
        st.error(f"No information found for branch {branch_value}")
        st.stop()

    subjects = branch_info["Subjects"]
    sub_names = [subject["SubjectName"] for subject in subjects]
    sub_codes = [subject["SubjectCode"] for subject in subjects]
    sub_creds = [int(subject["Credit"]) for subject in subjects]

    # Get internal_marks from session state or initialize with an empty dictionary
    if "internal_marks" not in st.session_state:
        st.session_state["internal_marks"] = {}
    internal_marks = st.session_state["internal_marks"]

    # Retrieve internal_marks for the current USN if it exists, otherwise use an empty dictionary
    internal_marks[usn] = retrieve_internal_marks(usn, semester) if check_usn_exists(usn) else {}

    # Ensure that internal_marks[usn] has the same keys as sub_names
    for subject in sub_names:
        if subject not in internal_marks[usn]:
            internal_marks[usn][subject] = 0

    def update_session_state(key, value=None):
        st.session_state[key] = st.session_state.get(key, value)

    for subject in sub_names:
        default_value = internal_marks[usn][subject]
        key = f"{usn}_{semester}_{subject}_input"
        # Initialize the session state for this key if it doesn't exist
        if key not in st.session_state:
            st.session_state[key] = default_value

        # Use the session state value for the number input
        st.number_input(
            label=f"{subject}",
            value=st.session_state[key],
            min_value=0,
            max_value=50,
            key=key,
            on_change=update_session_state,
            args=(key,)
        )

        # Update the internal marks dictionary
        internal_marks[usn][subject] = st.session_state[key]

    # Update the internal_marks dictionary in the session state with the current USN
    st.session_state["internal_marks"][usn] = internal_marks[usn]

    # Create the table with consistent lengths
    table = {
        "Subjects": sub_names,
        "Subject Codes": sub_codes,
        "Credits": sub_creds,
        "Internal Marks": [internal_marks[usn][subject] for subject in sub_names]
    }
    df = pd.DataFrame(table)
    st.write(df.style.set_table_styles(styles_gp).to_html(), unsafe_allow_html=True)
    st.write(" ")

    if check_usn_exists(usn):
        if st.button("Update"):
            message = update_student_marks(usn, semester, internal_marks[usn])
            if message:
                st.success("Marks updated successfully!")
            else:
                st.error("Failed to update marks!")

    return sub_names, sub_codes, sub_creds, list(internal_marks[usn].values())

def tab_3(sub_names, sub_codes, sub_creds, internal_marks):
    st.subheader("Grades and their Corresponding Scores")
    grade_values = grade_estimates(internal_marks)

    for subject, marks in zip(sub_names, internal_marks):
        data = {
            "Grades": ["O", "A+", "A", "B+", "B", "C", "P"],
            "Scores": [grade_values[grade][sub_names.index(subject)] for grade in ["O", "A+", "A", "B+", "B", "C", "P"]],
        }
        df = pd.DataFrame(data)
        
        st.write(f"###### {subject} : {marks}")

        s = df.set_index("Grades").T.style
        st.write(s.to_html(), unsafe_allow_html=True)

        st.write("  ")
        st.write("  ")

    return grade_values



def tab_4(sub_names, sub_codes, sub_creds, grade_values):
        st.subheader("Enter your Predicted Grade for each subjects")
        st.caption(
            "Mark the expected grades according to the previous tab and "
            "click on calculate to get your final credits and SGPA"
        )

        grade_in_each = []
        for i, sn in enumerate(sub_names):
            selected_grade = st.radio(sn, ["O", "A+", "A", "B+", "B", "C", "P", "F"], index=0, horizontal=True)
            grade_in_each.append(selected_grade)

    
        if st.button("Calculate"):
            st.write("<p class='mt'>Based on the above grades, this will be your final credits and SGPA</p>",
                 unsafe_allow_html=True)
            table = pd.DataFrame({
                "Subject": sub_names, "Grade": grade_in_each, "Credits": sub_creds,
            })

            st.write(table.style.set_table_styles(styles_gp).to_html(), unsafe_allow_html=True)

            sgpa = calculate_sgpa(sub_codes, sub_creds, grade_values, grade_in_each)
            st.write(f"<h3 class='mt'>Your SGPA is: {sgpa:.3f}</h2>", unsafe_allow_html=True)
            if sgpa is not None:
                st.balloons()


def home():
    with tab1:
        usn , semester, branch_value = tab_1()
        # print(usn, semester, branch)
    with tab2:
        sub_names, sub_codes, sub_creds, internal_marks = tab_2(usn , semester, branch_value)
        # print(sub_names, sub_codes, sub_creds, internal_marks)
    with tab3:
        grade_values = tab_3(sub_names, sub_codes, sub_creds, internal_marks)
    with tab4:
        tab_4(sub_names, sub_codes, sub_creds, grade_values)
    
if __name__ == "__main__":
    home()