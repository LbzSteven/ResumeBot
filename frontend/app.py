# frontend/appTry.py
import streamlit as st
import requests

from utils.constant import normalize_generate_type, education_option, generate_option, tone_option, fmt_option

st.title("🎯 Resume & Cover Letter Generator")


# generate_option = [
#                     "Resume (JSON bullets)",
#                     "Resume (Markdown)",
#                     "Cover Letter",
#                     "LinkedIn Summary",
#                     "Chinese"
#                         ]
#
# education_option = ["Undergraduate", "Master", "Doctoral"]
# tone_option = ["concise", "detailed", "persuasive"]

with st.form("resume_form"):
    name = st.text_input("Name")
    education = st.selectbox("Education", education_option)
    skills = st.text_area("Skills")
    experience = st.text_area("Work Experience")
    job_description = st.text_area("Target Job Description")

    generate_type = st.selectbox("Generate", options=generate_option)
    fmt_type = st.selectbox("Format", options=fmt_option)
    tone = st.selectbox("Tone", options=tone_option)
    requirement = st.text_area("Special Requirement")
    submitted = st.form_submit_button("Generate")

    fmt, type = normalize_generate_type(fmt_type,generate_type)

if submitted:
    payload = {
        "name": name,
        "education": education,
        "skills": skills,
        "experience": experience,
        "job_description": job_description,
        "tone": tone,
        "fmt": fmt,
        "type": type,
        "requirement": requirement,
    }
    res = requests.post("http://localhost:8000/generate", json=payload)

    st.subheader("Generated Result")
    st.write(res.json()["output"])