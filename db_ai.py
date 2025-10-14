import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# --- PAGE CONFIG ---
st.set_page_config(page_title="🏥 Hospital Management System", layout="wide")

# --- DATABASE FUNCTIONS ---
DB_NAME = "hospital.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create tables if they don't exist
    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        problem TEXT NOT NULL,
        doctor TEXT,
        specialization TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_doctor(name, specialization):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)", (name, specialization))
    conn.commit()
    conn.close()

def add_patient(name, age, problem, doctor, specialization):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO patients (name, age, problem, doctor, specialization)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, problem, doctor, specialization))
    conn.commit()
    conn.close()

def get_doctors():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM doctors", conn)
    conn.close()
    return df

def get_patients():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df

# --- DOCTOR ASSIGNMENT ---
def assign_doctor(problem):
    mapping = {
        "Fever": "General Physician",
        "Heart": "Cardiologist",
        "Skin": "Dermatologist",
        "Ortho": "Orthopedic",
        "Ent": "ENT Specialist"
    }
    specialization = mapping.get(problem, None)
    if specialization:
        doctors = get_doctors()
        doctor = doctors[doctors["specialization"] == specialization]
        if not doctor.empty:
            return doctor.iloc[0]
    return None

# --- INITIALIZE DATABASE ---
init_db()

# --- SIDEBAR MENU ---
st.sidebar.title("🏥 Hospital Management")
menu = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "👩‍⚕️ Doctors", "🧍 Patients", "📊 Analytics"]
)

# --- HOME PAGE ---
if menu == "🏠 Home":
    st.title("🏥 Hospital & Medical Facilities Management System")
    st.markdown("""
    Welcome to the **Hospital Management System Web App** built using **Streamlit + SQLite + Pandas + Matplotlib**.
    
    **Features:**
    - Manage Doctors & Patients  
    - Auto Doctor Assignment  
    - Interactive Analytics Dashboard  
    - Data Persistence using SQLite  
    - Simple, Beautiful, and Fast Web UI
    
    👈 Use the sidebar to navigate.
    """)

# --- DOCTORS PAGE ---
elif menu == "👩‍⚕️ Doctors":
    st.header("👨‍⚕️ Doctor Management")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Add Doctor")
        with st.form("add_doctor_form"):
            name = st.text_input("Doctor Name")
            specialization = st.text_input("Specialization")
            submit = st.form_submit_button("➕ Add Doctor")
            if submit and name and specialization:
                add_doctor(name, specialization)
                st.success(f"Doctor {name} added successfully!")

    with col2:
        st.subheader("View All Doctors")
        doctors = get_doctors()
        st.dataframe(doctors, use_container_width=True)

# --- PATIENTS PAGE ---
elif menu == "🧍 Patients":
    st.header("🧍 Patient Management")

    tab1, tab2 = st.tabs(["➕ Add Patient", "📋 View Patients"])
    
    with tab1:
        with st.form("add_patient_form"):
            name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            problem = st.selectbox("Health Issue", ["Fever", "Heart", "Skin", "Ortho", "Ent"])
            submitted = st.form_submit_button("Add Patient")

            if submitted and name:
                doc = assign_doctor(problem)
                add_patient(
                    name,
                    age,
                    problem,
                    doc["name"] if doc is not None else "Not Available",
                    doc["specialization"] if doc is not None else "N/A"
                )
                st.success(f"✅ Patient '{name}' added successfully!")
                if doc is not None:
                    st.info(f"Assigned Doctor: {doc['name']} ({doc['specialization']})")

    with tab2:
        patients = get_patients()
        if patients.empty:
            st.warning("No patients registered yet.")
        else:
            st.dataframe(patients, use_container_width=True)
            
            st.subheader("🔍 Search Patient")
            search_query = st.text_input("Enter Patient Name or ID")
            if search_query:
                if search_query.isdigit():
                    result = patients[patients["id"] == int(search_query)]
                else:
                    result = patients[patients["name"].str.contains(search_query, case=False, na=False)]
                if not result.empty:
                    st.dataframe(result, use_container_width=True)
                else:
                    st.error("No matching patient found.")

# --- ANALYTICS PAGE ---
elif menu == "📊 Analytics":
    st.header("📊 Patient Analytics Dashboard")
    patients = get_patients()
    if patients.empty:
        st.warning("No patient data available for analysis yet!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            avg_age = np.mean(patients["age"])
            st.metric("Average Patient Age", f"{avg_age:.2f} years")
        with col2:
            count = len(patients)
            st.metric("Total Patients", count)

        issue_count = patients["problem"].value_counts()
        st.subheader("🩺 Patients by Health Issue")
        st.bar_chart(issue_count)

        st.subheader("📈 Patient Distribution (Pie Chart)")
        fig, ax = plt.subplots()
        ax.pie(issue_count, labels=issue_count.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
