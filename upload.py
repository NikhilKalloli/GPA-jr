import pymongo
import streamlit as st
import json
from storage import *


@st.cache_resource 
def get_database_connection():
    client = pymongo.MongoClient(st.secrets["mongo"]["ATLAS_DB_URL"])
    db = client["sgpa-estimator"]
    collection = db["students"]
    return collection

def insert_ISE():
    print("Inserting ISE data")
    with open("subject_info.json", "r") as f:
        subject_info = json.load(f)

    ise_info = next((b for b in subject_info if b["Branch"] == "IS"), None)
    if not ise_info:
        print("ISE branch information not found in the JSON file")
        return False

    subjects = ise_info["Subjects"]
    internal_marks = {subject["SubjectName"]: 0 for subject in subjects}

    # Insert data for each ISE student
    for i in range(1, 156):
        usn = f"1MS22IS{i:03}"
        semester = 4
        branch = "IS"
        name = "ISE_Student"

        if not insert_student_data(usn, name, semester, branch, internal_marks):
            return False
        
    return True



def insert_CSE():
    print("Inserting CSE data")
    with open("subject_info.json", "r") as f:
        subject_info = json.load(f)

    # Find the CSE branch information
    cse_info = next((b for b in subject_info if b["Branch"] == "CS"), None)
    if not cse_info:
        print("CSE branch information not found in the JSON file")
        return False

    subjects = cse_info["Subjects"]
    internal_marks = {subject["SubjectName"]: 0 for subject in subjects}

    names_list = ['A DEEPTHI BANDI', 'A NANDINI', 'AAGNIK GHOSH', 'AARTHI P V', 'ABHAY BHANDARKAR', 'ABHISHEK JACOB SANTHOSH', 'ABHISHEK SIDDHARTH HOSMANI', 'ADARSH BENNUR', 'ADIL A', 'Aditi Mahajan', 'ADITRI B RAY', 'ADITYA G S', 'ADITYA J KRISHNAN', 'ADITYA KOTRESHA LINGASHETTY', 'ADITYA M', 'ADITYA MAHALINGAPPA HOSUR', 'ADITYA U YASHWANT', 'AISHWARYA R DONGAL', 'AJAY REDDY A', 'AKSHAY H M', 'AMIT ARUNKUMAR MADHABHAVI', 'AMOGH KALASAPURA', 'AMOGH R SURPURMATH', 'AMRUTA SHANKAR MANDI', 'ANIKET KUMAR SAH', 'ANIRUDH M', 'ANIRUDH S RAI', 'ANISHA AJIT', 'ANJALI R PAI', 'ANKIT SINGH', 'ANKUSH NARAYAN BALSE', 'ANUSHKA RAHUL PATIL', 'ARJUN SHETTY', 'ARUSA PARVAIZ', 'ARYAN KUMAR', 'ASHUTOSH KUMAR', 'ATHARVA MANCHALKAR', 'B KARTHIK', 'B P DEEPAK', 'BARSHA SHAH', 'BASAVARAJ BHAJANTRI', 'BATHINI BATHINANNA', 'BHASKARA S M', 'BRENDAN WOLFANGO PEREIRA', 'CHANDAN H K', 'CHIRAG SAHA', 'CHIRANTANA P', 'CHIRANTHAN M S', 'DARSHAN PRADEEPKUMAR CHOUTHAYI', 'DIVYANSHI JHA', 'DIYA D SHAH', 'EMILY SHERAPHIA SEBASTIAN', 'GAARGI N', 'GAURAV KUMAR', 'GULSHAN LAL', 'GURUPREETH N', 'HARIPRASAD B R', 'HARSH KUMAR', 'HARSHA RANI C', 'HARSHITA PUROHIT', 'HARSHITHA J S', 'HARSHVARDHAN MEHTA', 'HOOR PARVAIZ', 'IFRAH NAAZ', 'IMMAREDDY SUPRABATH REDDY', 'ISHA GUPTA', 'ISHA PRABHUDEV ALAGUNDAGI', 'Ishan Raj Upadhyay', 'ISHIKA DILIP MOHOL', 'J D RAGHU VEER', 'JAIVEER SINGH', 'JOANN MARY JOSEPH', 'JOEL AJITH THOMAS', 'Joshua Abhishek Leo', 'JYOTSNA P', 'KARTIK VINAY HEGDE', 'KRISH KUMAR', 'KUWAR AKSHAT', 'LEKHYA BIRIDEPALLI', 'MALLIKARJUN V SHAHAPURKAR', 'MANAS KARIR', 'MANASA M', 'MANGESH NARENDRA NESARIKAR', 'MANVENDRA PARMAR', 'MITESH S JAIN', 'MOODAMBAIL PAWAN', 'N RADHESH SHETTY', 'NANDITA NAYAK K', 'NARESH', 'NIHAREEKA MOHANTY', 'NIKHIL PRAKASH KALLOLI', 'NIKHIL S KALLARAKKAL', 'NIRMITH M R', 'NISHANTH K', 'NITIN MARUTI PARAMKAR', 'NITYASHREE R', 'P N PAVITHRA', 'P NITYA REDDY', 'Palak Saini', 'PATHAN IRBAZHUSSAIN MINHAJHUSEN', 'PAVAN KUMAR M', 'PAVITHRA K V', 'PRAJWAL PALADUGU', 'PRAMOD B BELAGALI', 'PRANSHU SARASWAT', 'PRATHVIRAJ GAWALI', 'PRATYUSH PAI', 'PRIYANSHU RANJAN SINGH', 'PURU', 'RAKESHVARMA K S', 'RAMEGOWDA M D', 'RASHMI B', 'RASHMITHA M', 'RIFAH BALQUEES', 'RISHIKESH J DHARWAR', 'RITIKESH KUMAR', 'RYAN AAHIL', 'S JEEVAN', 'SAHIL SAHAY', 'SAKSHI RAJU KUMBAR', 'SAMPADA B', 'SANCHIT VIJAY', 'SANGEETHA E', 'SANKET PATTANSHETTI', 'SASUMANA KUSHAL', 'SAURABH KUSHWAHA', 'SHAHBAAZ SALEEM', 'SHAMANTH M HIREMATH', 'SHANTANU PANDEY', 'SHARANYA M S', 'SHARANYA SANDEEP', 'SHASHANK AGARWAL', 'SHEIKH MANNAN JAVEED', 'SHIVAMANI R', 'SHIVANSH SHUKLA', 'SHRAVYA H', 'SHREESHANT BAHADUR SINGH', 'SHREYA RANGAPPAGARI', 'SHREYAS NAGABHUSHAN', 'SHREYAS SHIVALINGAPPA KADAPATTI', 'SHRINIDHI PAWAR', 'Siddhanth Pradhan', 'SIDDHARTH G ACHARYA', 'SNEHA', 'SOMNATH BANKAPURE', 'SOORAJ SAJJAN', 'SOURAV K', 'SUHAS BHAT BS', 'Surya Nirbhay Singh', 'SUVAN B U', 'TANU SHREE KUMAWAT', 'THARUN D S', 'TRIJAL SHINDE', 'VAIBHAV RAINA', 'VAISHAKH N Y', 'VARUN PATEL', 'VENKATESH K', 'VENNELA RUDRARAJU', 'VIBHA KODER', 'VINEET SURESH UPPALADINNI', 'VISHNU KUMAR K', 'YAMINI K', 'YASH SURESH GAVAS', 'YASHASVI KRISHNA B']

    # Insert data for each CSE student
    j=0
    for i in range(1, 165):
        usn = f"1MS22CS{i:03}"
        name = names_list[j]
        if j<164:
            j+=1
        semester = 4
        branch = "CS"
        if not insert_student_data(usn, name, semester, branch, internal_marks):
            return False
    
    return True



def main():
    insert_ISE()
    insert_CSE()

if __name__ == "__main__":
    main()



