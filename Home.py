import streamlit as st
import pandas as pd

# Define subjects as a global variable
SUBJECTS = [
    {"SubjectName": "Advanced Calculus and Modular Arithmetic", "SubjectCode": "MAC11", "Credit": 4},
    {"SubjectName": "Principles of Programming Using C", "SubjectCode": "PPC18", "Credit": 3},
    {"SubjectName": "Physics", "SubjectCode": "PYC12", "Credit": 3},
    {"SubjectName": "Electrical", "SubjectCode": "ESC13x", "Credit": 3},
    {"SubjectName": "Python", "SubjectCode": "PLC14x", "Credit": 3},
    {"SubjectName": "English", "SubjectCode": "HSCP15", "Credit": 1},
    {"SubjectName": "Kannada", "SubjectCode": "HSCP16", "Credit": 1},
    {"SubjectName": "A Scientific Approach to Health", "SubjectCode": "AECP17", "Credit": 1},
    {"SubjectName": "Physics Lab", "SubjectCode": "PYLC19", "Credit": 1},
]

st.set_page_config(page_title="Calculla - GPA Calculator", page_icon="📊", layout="centered")

# Initialize session state at startup
if 'initialized' not in st.session_state:
    st.session_state.internal_marks = {subject["SubjectName"]: 0 for subject in SUBJECTS}
    st.session_state.initialized = True

st.title("Calculla - GPA Calculator")
grade_to_gp = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0}
tab1, tab2, tab3 = st.tabs(["Enter Marks", "Grade Estimates", "Calculate GPA"])

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
    # Calculate grade points for each subject
    grade_points = [grade_to_gp[grade] for grade in grade_in_each]
    
    # Calculate weighted grade points
    weighted_gp = [gp * creds for gp, creds in zip(grade_points, sub_creds)]
    
    # Calculate SGPA
    total_weighted_gp = sum(weighted_gp)
    total_credits = sum(sub_creds)
    sgpa = round(total_weighted_gp / total_credits, 3)
    
    return sgpa

def tab_1():
    st.subheader("Enter Internal Marks")
    
    # Get subject information from global SUBJECTS
    sub_names = [subject["SubjectName"] for subject in SUBJECTS]
    sub_codes = [subject["SubjectCode"] for subject in SUBJECTS]
    sub_creds = [subject["Credit"] for subject in SUBJECTS]
    
    # Input fields for marks
    for subject in sub_names:
        st.session_state.internal_marks[subject] = st.number_input(
            label=f"{subject}",
            min_value=0,
            max_value=50,
            value=st.session_state.internal_marks[subject],
            key=f"input_{subject}"
        )
    
    # Display marks table
    table = {
        "Subjects": sub_names,
        "Subject Codes": sub_codes,
        "Credits": sub_creds,
        "Internal Marks": list(st.session_state.internal_marks.values())
    }
    df = pd.DataFrame(table)
    st.write(df)
    
    return sub_names, sub_codes, sub_creds, list(st.session_state.internal_marks.values())

def tab_2(sub_names, sub_codes, sub_creds, internal_marks):
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

def tab_3(sub_names, sub_codes, sub_creds, grade_values):
    st.subheader("Select Grades and Calculate SGPA")
    st.caption("Select your expected grade for each subject and click calculate to get your SGPA")
    
    grade_in_each = []
    for sn in sub_names:
        selected_grade = st.radio(sn, ["O", "A+", "A", "B+", "B", "C", "P", "F"], 
                                index=0, 
                                horizontal=True,
                                key=f"grade_{sn}")
        grade_in_each.append(selected_grade)
    
    if st.button("Calculate"):
        table = pd.DataFrame({
            "Subject": sub_names,
            "Grade": grade_in_each,
            "Credits": sub_creds,
        })
        
        st.write(table)
        sgpa = calculate_sgpa(sub_names, sub_creds, grade_values, grade_in_each)
        st.write(f"### Your SGPA is: {sgpa:.3f}")
        st.balloons()

def main():
    with tab1:
        sub_names, sub_codes, sub_creds, internal_marks = tab_1()
    with tab2:
        grade_values = tab_2(sub_names, sub_codes, sub_creds, internal_marks)
    with tab3:
        tab_3(sub_names, sub_codes, sub_creds, grade_values)

if __name__ == "__main__":
    main()