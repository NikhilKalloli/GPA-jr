import pandas as pd
import streamlit as st

from common import *

st.set_page_config(page_title="Calculla - Instruction & Working", page_icon="📊", layout="centered")
local_css("styles.css")
local_html("index.html")

table_body = [
	('border', '1.5px solid white'),
	('border-radius', '20px'),
]

hide_table_row_index = """
<style>
	thead tr th:first-child {display:none}
	tbody th {display:none}
</style>
"""

st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.title("Instruction and Working")

tab1, tab2, tab3 = st.tabs(["Instructions", "How its Calculated","Simple - Calculator"])

with tab1:
	st.write("1. Enter your USN, Semester and Branch in the Details tab")
	st.write("2. Enter your CIE marks in the CIE-Marks tab")
	st.write(
		"3. Switch to the Grades-Score tab, Here you can see the minimum marks to score in SEE to get respective grades.")
	st.write("4. Note down the expected grades for each subject")
	st.write("5. Switch to the Credit-GPA tab and select the grades based on the previous tab")
	st.write("6. Your SGPA will be displayed")
	st.write(
		"""
			<p>
			To get started 
			<a class="name" target="_self" href="/">Click Here</a>
			</p>
		""", unsafe_allow_html=True
	)

with tab2:
	st.write("The grading system is as follows:")
	creds = [10, 9, 8, 7, 6, 5, 4, 0]
	df = pd.DataFrame({
		"Marks Range": ["90 - 100", "80 - 89", "70 - 79", "60 - 69", "55 - 59", "50 - 54", "40 - 49", "0 - 39"],
		"Grade": ["O", "A+", "A", "B+", "B", "C", "P", "F"],
		"GPA": creds},
		index=None)
	st.write(df.style.set_table_styles(styles).to_html(), unsafe_allow_html=True)
	st.write("")
	st.subheader("Grade Point Average - GPA")
	st.write(
		"Grade Point Average (CGPA), both of which are important performance indices of the student. SGPA is equal to the sum of all the total points earned by the student in a given semester divided by the number of credits registered by the student in that semester. CGPA gives the sum of all the total points earned in all the previous semesters and the current semester divided by the number of credits registered in all these semesters.")

	st.markdown(
		"""
		#### Semester Grade point average - SGPA is calculated as follows: \n
		
		$$ \\frac{\sum (Course \\ Credits \\times Grade \\ Points) \\ all \\ Courses}{\sum (Course \\ Credits)\\ all \\ Courses} $$ \n
		
		""")
	# st.latex(r'''
	# 	SGPA = \frac{\sum Course Credits \times Grade Points}{\sum Total Course Credits}
	# 	''')
	st.write("#### Cumulative Grade point average - CGPA:", unsafe_allow_html=True)
	# st.latex(r'''
	# 	CGPA = \frac{\sum Course Credits \times Grade Points}{\sum Total Credits}
	# 	''')
	st.latex(r'''
		CGPA = \frac{Sum \ of \ all \ SGPA}{Total \ Credits \ earned}
		''')
	st.write("Note in CGPA : for all courses, excluding those with “F” and transitional grades until that semester")

with tab3:
	st.subheader("How much is average CIE marks for 50?")

	avg = st.slider("Average CIE marks", 0, 50, value=35, step=1)
	to_score = (90 - avg) * 2
	st.write("Following is the minimum marks you need to score in SEE to get respective grades")
	grades = [to_score, to_score - 20, to_score - 40, to_score - 60, to_score - 80, to_score - 100]
	for i in range(len(grades)):
		if grades[i] > 100:
			grades[i] = " "
	grade_letter = ["O", "A+", "A", "B+", "B", "C"]
	table_1 = pd.DataFrame({"Grade": grade_letter, "Marks": grades})
	st.write(table_1.style.hide(axis="index").set_table_styles(styles).to_html(), unsafe_allow_html=True)
	st.write("")
	st.write("Here is how its calculated :")
	st.write(
		f"You scored {avg}, then you need {to_score} in SEE to get O Grade. "
		f"Because half of {to_score} which is {to_score / 2} is added to {avg} equals to {(to_score / 2) + avg} "
		f"and that is minimum to get O Grade"
	)