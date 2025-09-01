import streamlit as st
import requests

st.set_page_config(page_title="FitPlanner", page_icon="💪", layout="centered")
st.title("FitPlanner (Stub) 💪")

with st.form("user_form"):
    name = st.text_input("Name", "Aditya")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    goal = st.selectbox("Goal", ["Fat loss", "Muscle gain", "Endurance"])
    submitted = st.form_submit_button("Generate Plan")

if submitted:
    try:
        resp = requests.post(
            "http://localhost:5000/api/generate-plan",
            json={"name": name, "age": int(age), "goal": goal},
            timeout=30
        )
        if resp.ok:
            data = resp.json()
            st.success(f"Plan for {data.get('user')}")
            st.subheader("Workout")
            for item in data["plan"]["workout"]:
                st.write("•", item)
            st.subheader("Meals")
            for item in data["plan"]["meals"]:
                st.write("•", item)
        else:
            st.error(f"API error: {resp.status_code} - {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
