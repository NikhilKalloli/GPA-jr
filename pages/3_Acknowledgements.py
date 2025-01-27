import streamlit as st

from common import *

st.set_page_config(page_title="Acknowledgements", page_icon="🤝", layout="centered")

local_css("styles.css")
local_html("index.html")

st.title("Acknowledgements")
st.write(
    """
    This project is built on top of the original Calculla, which was unfortunately no longer accessible due to new restrictions implemented by the college. The primary reason for Calculla's shutdown is the college's decision to enhance the security of its portal, preventing data scraping and brute force attacks.

    The author would like to thank the creators of original calculla <a class='name' href='https://www.linkedin.com/in/amithm3/'>Amith M</a> and <a class='name' href='https://www.linkedin.com/in/shravanrevanna/'>Shravan Revanna</a>  for their valuable guidance and support in the development of this project.

    Check out their blogs <a class='name' href='https://amithm3.hashnode.dev/calculla-the-over-engineered-gpa-calculator'>here</a> or <a class='name' href='https://shravanrevanna.hashnode.dev/calculla-the-next-level-gpa-calculator'>here</a> for more information.

    Here's the link to the original calculla: <a class='name' href='https://gpaestimator.streamlit.app/'>Calculla</a>

    Reach out to the author here <a class='name' href='https://x.com/NikhilKalloli'> Nikhil Kalloli</a> for any queries or concerns regarding this project.


	""", unsafe_allow_html=True
)