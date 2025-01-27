import streamlit as st

from common import *

st.set_page_config(page_title="Terms and Disclaimer", page_icon="👨‍💻", layout="centered")

local_css("styles.css")
local_html("index.html")

st.title("Terms and Disclaimer")

st.write(
	"""    
	By using our app, you acknowledge and agree that we store certain information entered by you, such as internal marks, 
	in order to provide faster access to that information upon subsequent use of the app. 
	
    
	By using our app, you agree to indemnify and hold us harmless from any loss or damage that may result from any unauthorized access to your personal information, 
	whether due to our app's vulnerabilities or your own actions.

	We reserve the right to update these Terms and Conditions at any time, 
	and we encourage you to review them periodically. 
	Your continued use of our app after any changes to these Terms and Conditions will constitute your acceptance of the revised terms.

	The authors have taken all possible measures to ensure that the results provided by our tool are as accurate as possible.
	However, we cannot guarantee the accuracy, completeness, or reliability of the information provided. 
	Therefore, we will not be liable for any damages or losses that may arise from the use of the tool or the information provided by it.
	It is the responsibility of the user to verify the accuracy of the information provided and to use it at their own risk.
	By using the app, you acknowledge and agree to these terms and conditions.
	
	If you have any questions or concerns about our data storage policy, please contact the author
	<a class='name' href='https://x.com/NikhilKalloli/'>here</a> 
	""", unsafe_allow_html=True
)
