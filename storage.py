import pymongo
import streamlit as st


@st.cache_resource 
def get_database_connection():
    client = pymongo.MongoClient(st.secrets["mongo"]["ATLAS_DB_URL"])
    db = client["sgpa-estimator"]
    collection = db["students"]
    return collection


def insert_student_data(usn, name, semester, branch, internal_marks):
    try:
        collection = get_database_connection()
        student = {
            "usn": usn,
            "name": name, 
            "semester": semester,
            "branch": branch,
            "internal_marks": internal_marks
        }
        result = collection.insert_one(student)
        print("Inserted student record with ID:", result.inserted_id)
        return True
    except Exception as e:
        print("Failed to insert student record:", e)
        return False




def retrieve_internal_marks(usn, semester):
    collection = get_database_connection()

    # query = {"usn": usn, "semester": semester}
    query = {"usn": usn}
    student_data = collection.find_one(query)

    if student_data:
        # print(student_data["internal_marks"])
        return student_data["internal_marks"]
    else:
        return {}



def update_student_marks(usn, semester, internal_marks):
    collection = get_database_connection()
    filter_query = {"usn": usn}

    # doc= collection.find_one(filter_query)
    # print(doc)
    update_operation = {"$set": {"internal_marks": internal_marks}}

    result = collection.update_one(filter_query, update_operation)
    # print(result)

    if result.modified_count == 1:
        print("Marks updated Successfully")
        return True
    else:
        print("No student found with the provided USN and semester.")
        return False
   


def delete_student_data(usn, semester):
    collection = get_database_connection()
    filter_query = {"usn": usn}
    
    result = collection.delete_one(filter_query)
    print(result)

    if result.deleted_count == 1:
        print("Student data deleted successfully.")
        return True
    else:
        print("No student found with the provided USN and semester.")
        return False
    

def delete_all():
    """Delete all documents from the collection."""
    collection = get_database_connection() 
    try:
        result = collection.delete_many({})
        return True  
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  


def check_usn_exists(usn):
    collection = get_database_connection()
    query = {"usn": usn}
    student_data = collection.find_one(query)
    return True if student_data else False

def get_student_name(usn):
    collection = get_database_connection()
    query = {"usn": usn}
    student_data = collection.find_one(query)
    return student_data["name"] if student_data else "Unknown"

if __name__ == "__main__":
    insert_student_data()
    retrieve_internal_marks()
    update_student_marks()