# frontend/appTry.py
import streamlit as st
import requests
import json
import os
from utils.constant import *
from utils.json_util import list_default_files, load_defaults_from_file, save_defaults_to_timestamped_file
from utils.output_util import save_output_to_file


st.title("🎯 Resume & Cover Letter Generator")
# --- 1. 载入当前默认值（初始）
if "current_defaults" not in st.session_state:
    st.session_state["current_defaults"] = {}

# --- 2. 导入旧默认值
st.sidebar.subheader("Import history as input")
available_files = list_default_files()
selected_file = st.sidebar.selectbox("Choose this history", options=available_files)
if st.sidebar.button("📥 Import this history"):
    st.session_state["current_defaults"] = load_defaults_from_file(selected_file)
    st.success(f"Imported：{selected_file}")
    st.session_state["imported"] = True




def load_defaults(path="./default_input.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


default_input = st.session_state.get("current_defaults", {})
imported = st.session_state.get("imported", False)




def selectbox_with_default(label, options, default_value):
    index = options.index(default_value) if default_value in options else 0
    return st.selectbox(label, options, index=index)

with st.form("resume_form"):
    name = st.text_input("Name", value=default_input.get("name", ""))

    education = selectbox_with_default("Education", education_option, default_input.get("education", ""))
    skills = st.text_area("Skills", value=default_input.get("skills", ""))
    experience = st.text_area("Work Experience", value=default_input.get("experience", ""))
    job_description = st.text_area("Target Job Description", value=default_input.get("job_description", ""))

    generate_type = selectbox_with_default("Type", generate_option, default_input.get("type", ""))
    fmt_type = selectbox_with_default("Format", fmt_option, default_input.get("format", ""))
    tone = selectbox_with_default("Tone", tone_option, default_input.get("tone", ""))
    requirement = st.text_area("Special Requirement", value=default_input.get("requirement", ""))
    submitted = st.form_submit_button("Generate")

    fmt, type = normalize_generate_type(fmt_type, generate_type)


if imported:
    if st.sidebar.button("💾 Save as new default"):
        current_input = {
            "name": name,
            "education": education,
            "skills": skills,
            "experience": experience,
            "job_description": job_description,
            "generate_type": generate_type,
            "tone": tone,
            "requirement": requirement,
        }

        save_path = save_defaults_to_timestamped_file(current_input)
        st.session_state["just_saved"] = save_path  # 可选：用于状态传递
        st.rerun()

    if "just_saved" in st.session_state:
        st.success(f"✅ 当前输入已保存：{st.session_state['just_saved']}")
        del st.session_state["just_saved"]



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

    st.subheader("Generated Result (Editable)")

    # 存储第一次生成结果 Streamlit 的 st.text_area() 是 声明式组件，每次刷新页面（如点击按钮）都会重新执行所有代码。
    st.session_state["generated_output"] = res.json()["output"]



if "generated_output" in st.session_state:
    st.session_state["generated_output"] = st.text_area(
        "You can revise the generated content below:",
        value=st.session_state["generated_output"],
        key="editable_area",
        height=300
    )

    if st.button("Save Final Version"):
        from utils.output_util import save_output_to_file

        file_path = save_output_to_file(content=st.session_state["generated_output"])
        st.success(f"✅ Output saved successfully at {file_path}")
