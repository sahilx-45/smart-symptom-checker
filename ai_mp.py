from tabulate import tabulate
from colorama import Fore, Style, init
import time
init(autoreset=True)

class Hospital:
    def __init__(self):
        self.doctors = [
            {"ID": 1, "Name": "Dr. Mehta", "Specialization": "General Physician"},
            {"ID": 2, "Name": "Dr. Sharma", "Specialization": "Cardiologist"},
            {"ID": 3, "Name": "Dr. Patel", "Specialization": "Dermatologist"},
            {"ID": 4, "Name": "Dr. Gupta", "Specialization": "Orthopedic"},
            {"ID": 5, "Name": "Dr. Nair", "Specialization": "ENT Specialist"},
        ]
        self.patients = []

    def loading(self, msg="Processing"):
        for i in range(3):
            print(Fore.CYAN + msg + "." * (i + 1), end="\r")
            time.sleep(0.3)
        print(" " * 30, end="\r")

    def add_patient(self):
        print(Fore.YELLOW + "\nEnter Patient Details:")
        name = input("Name: ")
        age = input("Age: ")
        problem = input("Health Issue (Fever/Heart/Skin/Ortho/ENT): ").strip().capitalize()

        doctor = self.assign_doctor(problem)
        patient_id = len(self.patients) + 1

        patient = {
            "ID": patient_id,
            "Name": name,
            "Age": age,
            "Problem": problem,
            "Doctor": doctor["Name"] if doctor else "Not Available",
            "Specialization": doctor["Specialization"] if doctor else "N/A"
        }
        self.loading("Adding patient")
        self.patients.append(patient)
        print(Fore.GREEN + f"\n✅ Patient '{name}' successfully registered!")
        print(Fore.CYAN + f"Assigned Doctor: {doctor['Name']} ({doctor['Specialization']})" if doctor else "No doctor available")

    def assign_doctor(self, problem):
        mapping = {
            "Fever": "General Physician",
            "Heart": "Cardiologist",
            "Skin": "Dermatologist",
            "Ortho": "Orthopedic",
            "Ent": "ENT Specialist"
        }
        specialization = mapping.get(problem, None)
        if specialization:
            for doc in self.doctors:
                if doc["Specialization"] == specialization:
                    return doc
        return None

    def show_doctors(self):
        print(Fore.YELLOW + "\n--- List of Available Doctors ---")
        print(tabulate(self.doctors, headers="keys", tablefmt="fancy_grid"))

    def show_patients(self):
        print(Fore.YELLOW + "\n--- Registered Patients ---")
        if not self.patients:
            print(Fore.RED + "No patients registered yet.")
            return
        print(tabulate(self.patients, headers="keys", tablefmt="fancy_grid"))

    def search_patient(self):
        key = input(Fore.CYAN + "\nEnter patient name or ID to search: ").strip()
        found = []
        for p in self.patients:
            if str(p["ID"]) == key or key.lower() in p["Name"].lower():
                found.append(p)
        if found:
            print(Fore.YELLOW + "\n--- Search Results ---")
            print(tabulate(found, headers="keys", tablefmt="fancy_grid"))
        else:
            print(Fore.RED + "No patient found with that name or ID.")

    def add_doctor(self):
        print(Fore.YELLOW + "\nEnter Doctor Details:")
        name = input("Name: ")
        specialization = input("Specialization: ")
        doc_id = len(self.doctors) + 1
        doctor = {"ID": doc_id, "Name": name, "Specialization": specialization}
        self.loading("Adding doctor")
        self.doctors.append(doctor)
        print(Fore.GREEN + f"\n✅ Doctor '{name}' successfully added!")

def main_menu():
    hospital = Hospital()
    while True:
        print(Fore.MAGENTA + "\n==============================")
        print(Fore.CYAN + "🏥  HOSPITAL MANAGEMENT SYSTEM")
        print(Fore.MAGENTA + "==============================")
        print(Fore.YELLOW + """
1️⃣  View Doctors
2️⃣  Add Doctor
3️⃣  Add Patient
4️⃣  View Patients
5️⃣  Search Patient
6️⃣  Exit
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
            print(Fore.GREEN + "\nThank you for using Hospital Management System. Stay Healthy! 💚")
            break
        else:
            print(Fore.RED + "Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
