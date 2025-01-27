
from pymongo.mongo_client import MongoClient
import streamlit as st


uri = st.secrets.mongo.ATLAS_DB_URL

# Create a new client and connect to the server
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)