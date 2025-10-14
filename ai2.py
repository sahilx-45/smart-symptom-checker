import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
from tabulate import tabulate
import time

init(autoreset=True)

class Hospital:
    def __init__(self):
        # Predefined doctors
        self.doctors = pd.DataFrame([
            {"ID": 1, "Name": "Dr. Mehta", "Specialization": "General Physician"},
            {"ID": 2, "Name": "Dr. Sharma", "Specialization": "Cardiologist"},
            {"ID": 3, "Name": "Dr. Patel", "Specialization": "Dermatologist"},
            {"ID": 4, "Name": "Dr. Gupta", "Specialization": "Orthopedic"},
            {"ID": 5, "Name": "Dr. Nair", "Specialization": "ENT Specialist"}
        ])
        self.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Problem", "Doctor", "Specialization"])

    def loading(self, msg="Processing"):
        for i in range(3):
            print(Fore.CYAN + msg + "." * (i + 1), end="\r")
            time.sleep(0.3)
        print(" " * 30, end="\r")

    def assign_doctor(self, problem):
        mapping = {
            "Fever": "General Physician",
            "Heart": "Cardiologist",
            "Skin": "Dermatologist",
            "Ortho": "Orthopedic",
            "Ent": "ENT Specialist"
        }
        spec = mapping.get(problem.capitalize(), None)
        if spec:
            doctor = self.doctors[self.doctors["Specialization"] == spec]
            if not doctor.empty:
                return doctor.iloc[0]
        return None

    def add_patient(self):
        print(Fore.YELLOW + "\nEnter Patient Details:")
        name = input("Name: ")
        age = int(input("Age: "))
        problem = input("Health Issue (Fever/Heart/Skin/Ortho/ENT): ").strip()

        doctor = self.assign_doctor(problem)
        self.loading("Registering patient")

        new_patient = {
            "ID": len(self.patients) + 1,
            "Name": name,
            "Age": age,
            "Problem": problem.capitalize(),
            "Doctor": doctor["Name"] if doctor is not None else "Not Available",
            "Specialization": doctor["Specialization"] if doctor is not None else "N/A"
        }
        self.patients = pd.concat([self.patients, pd.DataFrame([new_patient])], ignore_index=True)

        print(Fore.GREEN + f"\n✅ Patient '{name}' successfully added!")
        if doctor is not None:
            print(Fore.CYAN + f"Assigned Doctor: {doctor['Name']} ({doctor['Specialization']})")

    def show_doctors(self):
        print(Fore.YELLOW + "\n--- Available Doctors ---")
        print(tabulate(self.doctors, headers='keys', tablefmt='fancy_grid', showindex=False))

    def show_patients(self):
        print(Fore.YELLOW + "\n--- Registered Patients ---")
        if self.patients.empty:
            print(Fore.RED + "No patients registered yet.")
        else:
            print(tabulate(self.patients, headers='keys', tablefmt='fancy_grid', showindex=False))

    def search_patient(self):
        key = input(Fore.CYAN + "\nEnter Patient Name or ID to Search: ").strip()
        if key.isdigit():
            result = self.patients[self.patients["ID"] == int(key)]
        else:
            result = self.patients[self.patients["Name"].str.contains(key, case=False, na=False)]

        if result.empty:
            print(Fore.RED + "No matching patient found.")
        else:
            print(Fore.YELLOW + "\n--- Search Result ---")
            print(tabulate(result, headers='keys', tablefmt='fancy_grid', showindex=False))

    def add_doctor(self):
        print(Fore.YELLOW + "\nEnter Doctor Details:")
        name = input("Name: ")
        specialization = input("Specialization: ")
        doc_id = len(self.doctors) + 1
        new_doc = pd.DataFrame([{"ID": doc_id, "Name": name, "Specialization": specialization}])
        self.doctors = pd.concat([self.doctors, new_doc], ignore_index=True)
        self.loading("Adding doctor")
        print(Fore.GREEN + f"\n✅ Doctor '{name}' successfully added!")

    def analytics(self):
        if self.patients.empty:
            print(Fore.RED + "\nNo data to analyze yet!")
            return
        
        print(Fore.YELLOW + "\n--- Patient Analytics ---")
        issue_count = self.patients["Problem"].value_counts()
        avg_age = np.mean(self.patients["Age"])
        
        print(Fore.CYAN + f"\nAverage Patient Age: {avg_age:.2f} years")
        print("\nPatients per Health Issue:")
        print(issue_count.to_string())

        plt.figure(figsize=(8, 4))
        issue_count.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title("Number of Patients by Health Issue")
        plt.xlabel("Health Issue")
        plt.ylabel("Count")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

def main_menu():
    hospital = Hospital()
    while True:
        print(Fore.MAGENTA + "\n==============================")
        print(Fore.CYAN + "🏥  HOSPITAL MANAGEMENT SYSTEM (Analytics Edition)")
        print(Fore.MAGENTA + "==============================")
        print(Fore.YELLOW + """
1️⃣  View Doctors
2️⃣  Add Doctor
3️⃣  Add Patient
4️⃣  View Patients
5️⃣  Search Patient
6️⃣  Analytics Dashboard
7️⃣  Exit
""")
        choice = input(Fore.CYAN + "Enter your choice: ").strip()

        if choice == "1":
            hospital.show_doctors()
        elif choice == "2":
            hospital.add_doctor()
        elif choice == "3":
            hospital.add_patient()
        elif choice == "4":
            hospital.show_patients()
        elif choice == "5":
            hospital.search_patient()
        elif choice == "6":
            hospital.analytics()
        elif choice == "7":
            print(Fore.GREEN + "\nThank you for using Hospital Management System! Stay Healthy 💚")
            break
        else:
            print(Fore.RED + "Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()
