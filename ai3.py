import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="🏥 Hospital Management System", layout="wide")

# --- SESSION STATE ---
if "doctors" not in st.session_state:
    st.session_state.doctors = pd.DataFrame([
        {"ID": 1, "Name": "Dr. Mehta", "Specialization": "General Physician"},
        {"ID": 2, "Name": "Dr. Sharma", "Specialization": "Cardiologist"},
        {"ID": 3, "Name": "Dr. Patel", "Specialization": "Dermatologist"},
        {"ID": 4, "Name": "Dr. Gupta", "Specialization": "Orthopedic"},
        {"ID": 5, "Name": "Dr. Nair", "Specialization": "ENT Specialist"},
    ])

if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Problem", "Doctor", "Specialization"])

# --- HELPER FUNCTION ---
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
        doctor = st.session_state.doctors[st.session_state.doctors["Specialization"] == specialization]
        if not doctor.empty:
            return doctor.iloc[0]
    return None

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
    Welcome to the **Hospital Management System Web App** built using **Streamlit + Pandas + NumPy + Matplotlib**.
    
    **Features:**
    - Manage Doctors & Patients  
    - Auto Doctor Assignment  
    - Interactive Analytics Dashboard  
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
                new_id = len(st.session_state.doctors) + 1
                new_doc = pd.DataFrame([{"ID": new_id, "Name": name, "Specialization": specialization}])
                st.session_state.doctors = pd.concat([st.session_state.doctors, new_doc], ignore_index=True)
                st.success(f"Doctor {name} added successfully!")

    with col2:
        st.subheader("View All Doctors")
        st.dataframe(st.session_state.doctors, use_container_width=True)

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
                new_id = len(st.session_state.patients) + 1
                new_patient = {
                    "ID": new_id,
                    "Name": name,
                    "Age": age,
                    "Problem": problem,
                    "Doctor": doc["Name"] if doc is not None else "Not Available",
                    "Specialization": doc["Specialization"] if doc is not None else "N/A"
                }
                st.session_state.patients = pd.concat(
                    [st.session_state.patients, pd.DataFrame([new_patient])],
                    ignore_index=True
                )
                st.success(f"✅ Patient '{name}' added successfully!")
                if doc is not None:
                    st.info(f"Assigned Doctor: {doc['Name']} ({doc['Specialization']})")

    with tab2:
        if st.session_state.patients.empty:
            st.warning("No patients registered yet.")
        else:
            st.dataframe(st.session_state.patients, use_container_width=True)
            
            # Search functionality
            st.subheader("🔍 Search Patient")
            search_query = st.text_input("Enter Patient Name or ID")
            if search_query:
                if search_query.isdigit():
                    result = st.session_state.patients[st.session_state.patients["ID"] == int(search_query)]
                else:
                    result = st.session_state.patients[
                        st.session_state.patients["Name"].str.contains(search_query, case=False, na=False)
                    ]
                if not result.empty:
                    st.dataframe(result, use_container_width=True)
                else:
                    st.error("No matching patient found.")

# --- ANALYTICS PAGE ---
elif menu == "📊 Analytics":
    st.header("📊 Patient Analytics Dashboard")

    if st.session_state.patients.empty:
        st.warning("No patient data available for analysis yet!")
    else:
        patients = st.session_state.patients
        col1, col2 = st.columns(2)
        
        with col1:
            avg_age = np.mean(patients["Age"])
            st.metric("Average Patient Age", f"{avg_age:.2f} years")
        
        with col2:
            count = len(patients)
            st.metric("Total Patients", count)
        
        # Count patients by problem
        issue_count = patients["Problem"].value_counts()
        st.subheader("🩺 Patients by Health Issue")
        st.bar_chart(issue_count)

        # Matplotlib chart (pie)
        st.subheader("📈 Patient Distribution (Pie Chart)")
        fig, ax = plt.subplots()
        ax.pie(issue_count, labels=issue_count.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
