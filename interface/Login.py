import streamlit as st
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

st.title("Music Learning App - Authentication")


def register():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    password2 = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        data = {"username": username, "password1": password, "password2": password2}
        response = requests.post(f"{BASE_URL}/register/", json=data)
        if response.status_code == 201:
            st.success("Registered successfully! Please log in.")
        else:
            st.error(f"Error: {response.json()}")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        data = {"username": username, "password": password}
        response = requests.post(f"{BASE_URL}/login/", json=data)
        if response.status_code == 200:
            token = response.json().get('token')
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['auth_token'] = token
            st.success(f"Welcome, {username}!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.subheader("Logout")
    if st.button("Logout"):
        response = requests.post(f"{BASE_URL}/logout/")
        if response.status_code == 200:
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.success("Logged out successfully")
            time.sleep(1)
            st.rerun()


if "logged_in" not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
if st.session_state['logged_in']:
    st.write(f"**Logged in as:** {st.session_state['username']}")
    logout()
else:
    option = st.radio("Choose an option", ("Login", "Register"))
    if option == "Login":
        login()
    elif option == "Register":
        register()
