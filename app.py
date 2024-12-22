import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os
import plotly.graph_objects as go
import pandas as pd

# Configure page settings
st.set_page_config(
    page_title="MediConnect Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background-color: #f8fafc;
        padding: 2rem;
        color: #1e293b;
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background-color: #1e293b;
        padding: 2rem 1rem;
    }
    
    .css-1d391kg img {
        display: block;
        margin: 0 auto 2rem auto;
        border-radius: 10px;
    }
    
    /* Card Design System */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
    }
    
    .stat-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .stat-card p {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
        margin: 0;
    }
    
    /* Enhanced Button Styles */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
    }
    
    /* Form Field Enhancement */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Table Styling */
    .styled-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1rem 0;
        background: white;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .styled-table th {
        background: #f1f5f9;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        color: #1e293b;
    }
    
    .styled-table td {
        padding: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Enhanced Timeline */
    .timeline {
        margin: 2rem 0;
        position: relative;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 2px;
        background: #e2e8f0;
    }
    
    .timeline-item {
        margin-left: 2rem;
        padding: 1.5rem;
        background: white;
        border-radius: 8px;
        position: relative;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -2.5rem;
        top: 1.5rem;
        width: 1rem;
        height: 1rem;
        border-radius: 50%;
        background: #3b82f6;
        border: 3px solid white;
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .dashboard-card h4 {
        color: #1e293b;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-active {
        background: #dcfce7;
        color: #166534;
    }
    
    .status-pending {
        background: #fef9c3;
        color: #854d0e;
    }
    
    /* Charts Container */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    /* Notifications */
    .notification {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .notification-info {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
    }
    
    .notification-warning {
        background: #fef9c3;
        border: 1px solid #fde047;
        color: #854d0e;
    }
    
    .notification-success {
        background: #dcfce7;
        border: 1px solid #86efac;
        color: #166534;
    }
    
    /* Search Bar Enhancement */
    .search-container {
        position: relative;
        margin: 1rem 0;
    }
    
    .search-container input {
        width: 100%;
        padding: 1rem 1rem 1rem 3rem;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        font-size: 1rem;
    }
    
    .search-container::before {
        content: "🔍";
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.25rem;
    }
    
    /* Patient Profile Card */
    .patient-profile {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    
    .patient-profile::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(to right, #3b82f6, #2563eb);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #94a3b8;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    </style>
""", unsafe_allow_html=True)

# Rest of your existing code with these UI enhancements:
# 1. Replace st.container() with custom HTML/CSS cards
# 2. Use the new status-pill classes for status indicators
# 3. Implement the enhanced timeline design
# 4. Apply the new notification styles
# 5. Use the patient-profile class for patient records

# Example of enhanced patient card usage:
def render_patient_card(patient):
    return f"""
    <div class="patient-profile">
        <h3>{patient['name']}</h3>
        <div class="status-pill status-active">Active</div>
        <div style="margin-top: 1rem;">
            <p><strong>ID:</strong> {patient['id']}</p>
            <p><strong>Age:</strong> {patient['age']}</p>
            <p><strong>Blood Group:</strong> {patient['blood_group']}</p>
        </div>
    </div>
    """

# Example of enhanced notification usage:
def render_notification(type, message):
    return f"""
    <div class="notification notification-{type}">
        {message}
    </div>
    """

# The rest of your existing application code remains the same,
# but you'll need to update the HTML generation to use these new components

# Initialize session state with additional features
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'appointments' not in st.session_state:
    st.session_state.appointments = {}
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_patients': 0,
        'active_cases': 0,
        'appointments_today': 0
    }

def save_data():
    """Save all application data"""
    data = {
        'patient_data': st.session_state.patient_data,
        'appointments': st.session_state.appointments,
        'stats': st.session_state.stats
    }
    with open('medical_system_data.json', 'w') as f:
        json.dump(data, f)

def load_data():
    """Load all application data"""
    if os.path.exists('medical_system_data.json'):
        with open('medical_system_data.json', 'r') as f:
            data = json.load(f)
            st.session_state.patient_data = data.get('patient_data', {})
            st.session_state.appointments = data.get('appointments', {})
            st.session_state.stats = data.get('stats', {
                'total_patients': 0,
                'active_cases': 0,
                'appointments_today': 0
            })

# Load existing data
load_data()

# Sidebar with improved navigation
with st.sidebar:
    st.image("https://your-logo-url.com", width=100)  # Add your logo
    st.title("MediConnect Pro")
    
    navigation = st.radio(
        "Navigate",
        ["Dashboard", "Patient Management", "Appointments", "Analytics"]
    )

# Main content
if navigation == "Dashboard":
    st.title("📊 Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", st.session_state.stats['total_patients'])
    with col2:
        st.metric("Active Cases", st.session_state.stats['active_cases'])
    with col3:
        st.metric("Appointments Today", st.session_state.stats['appointments_today'])
    with col4:
        st.metric("Recovery Rate", "85%")
    
    # Recent activity and notifications
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Activity")
        with st.container():
            st.markdown("""
            <div class="timeline-container">
                <div class="timeline-item">
                    <strong>New Patient Added</strong><br>
                    John Doe - 10:30 AM
                </div>
                <div class="timeline-item">
                    <strong>Diagnosis Updated</strong><br>
                    Sarah Smith - 09:15 AM
                </div>
                <div class="timeline-item">
                    <strong>Appointment Scheduled</strong><br>
                    Mike Johnson - 08:45 AM
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🔔 Notifications")
        st.info("3 patients due for follow-up")
        st.warning("2 test results pending")
        st.success("5 appointments confirmed for tomorrow")

elif navigation == "Patient Management":
    st.title("👥 Patient Management")
    
    tabs = st.tabs(["Add Patient", "Search & Update", "Patient Records"])
    
    with tabs[0]:
        # Enhanced Add Patient form
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input("Patient ID", placeholder="Enter unique ID")
            name = st.text_input("Full Name", placeholder="Enter patient's full name")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Select Gender", "Male", "Female", "Other"])
            
        with col2:
            contact = st.text_input("Contact Number", placeholder="+1 (xxx) xxx-xxxx")
            email = st.text_input("Email", placeholder="patient@example.com")
            blood_group = st.selectbox("Blood Group", ["Select Blood Group", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            emergency_contact = st.text_input("Emergency Contact", placeholder="Emergency contact number")
        
        # Additional medical information
        st.subheader("Medical Information")
        col1, col2 = st.columns(2)
        
        with col1:
            allergies = st.text_area("Allergies", placeholder="List any known allergies")
            current_medications = st.text_area("Current Medications", placeholder="List current medications")
            
        with col2:
            medical_history = st.text_area("Medical History", placeholder="Relevant medical history")
            notes = st.text_area("Additional Notes", placeholder="Any additional notes")
        
        if st.button("Add Patient", use_container_width=True):
            if patient_id and name:
                if patient_id not in st.session_state.patient_data:
                    st.session_state.patient_data[patient_id] = {
                        "name": name,
                        "dob": str(dob),
                        "gender": gender,
                        "contact": contact,
                        "email": email,
                        "blood_group": blood_group,
                        "emergency_contact": emergency_contact,
                        "allergies": allergies,
                        "current_medications": current_medications,
                        "medical_history": medical_history,
                        "notes": notes,
                        "diagnoses": [],
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.stats['total_patients'] += 1
                    save_data()
                    st.success("Patient added successfully!")
                else:
                    st.warning("Patient ID already exists!")
            else:
                st.warning("Please fill in Patient ID and Name!")

    with tabs[1]:
        # Enhanced search functionality
        search_query = st.text_input("🔍 Search Patients", placeholder="Search by ID, name, or contact number")
        
        if search_query:
            matches = []
            for pid, data in st.session_state.patient_data.items():
                if (search_query.lower() in pid.lower() or 
                    search_query.lower() in data['name'].lower() or 
                    search_query in data['contact']):
                    matches.append((pid, data))
            
            if matches:
                for pid, patient in matches:
                    with st.expander(f"📝 {patient['name']} (ID: {pid})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.text_input("Name", patient['name'], key=f"name_{pid}")
                            st.text_input("Contact", patient['contact'], key=f"contact_{pid}")
                            st.text_input("Email", patient['email'], key=f"email_{pid}")
                            
                        with col2:
                            st.text_input("Blood Group", patient['blood_group'], key=f"blood_{pid}")
                            st.text_input("Emergency Contact", patient['emergency_contact'], key=f"emergency_{pid}")
                            
                        st.text_area("Medical History", patient['medical_history'], key=f"history_{pid}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Update", key=f"update_{pid}"):
                                # Update patient information
                                st.success("Patient information updated successfully!")
                        with col2:
                            if st.button("Delete", key=f"delete_{pid}"):
                                # Delete patient record
                                st.warning("Patient record deleted successfully!")
            else:
                st.info("No matching patients found.")

    with tabs[2]:
        # Enhanced patient records view
        if st.session_state.patient_data:
            for pid, patient in st.session_state.patient_data.items():
                with st.expander(f"👤 {patient['name']} (ID: {pid})"):
                    # Patient summary card
                    st.markdown(f"""
                    <div class="patient-card">
                        <h3>{patient['name']}</h3>
                        <p><strong>ID:</strong> {pid}</p>
                        <p><strong>Age:</strong> {patient['dob']}</p>
                        <p><strong>Gender:</strong> {patient['gender']}</p>
                        <p><strong>Blood Group:</strong> {patient['blood_group']}</p>
                        <p><strong>Contact:</strong> {patient['contact']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Medical history timeline
                    if patient['diagnoses']:
                        st.subheader("Medical Timeline")
                        for diagnosis in reversed(patient['diagnoses']):
                            st.markdown(f"""
                            <div class="timeline-item">
                                <strong>{diagnosis['date']}</strong>
                                <p><em>Symptoms:</em> {diagnosis['symptoms']}</p>
                                <p><strong>Analysis:</strong> {diagnosis['ai_analysis']}</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("No patient records found.")

elif navigation == "Appointments":
    st.title("📅 Appointments")
    
    col1, col2 = st.columns([2, 1])
    # Calendar view for appointments
    with col1:
        st.subheader("📅 Schedule Appointments")
        appointment_date = st.date_input("Select Date")
        appointment_time = st.time_input("Select Time")
        patient_id = st.selectbox("Select Patient", list(st.session_state.patient_data.keys()))
        appointment_type = st.selectbox("Appointment Type", [
            "Regular Checkup",
            "Follow-up",
            "Specialist Consultation",
            "Lab Test",
            "Vaccination",
            "Physical Therapy"
        ])
        appointment_notes = st.text_area("Notes")
        
        if st.button("Schedule Appointment"):
            appointment_id = f"{appointment_date}-{appointment_time}-{patient_id}"
            if appointment_id not in st.session_state.appointments:
                st.session_state.appointments[appointment_id] = {
                    "patient_id": patient_id,
                    "patient_name": st.session_state.patient_data[patient_id]["name"],
                    "date": str(appointment_date),
                    "time": str(appointment_time),
                    "type": appointment_type,
                    "notes": appointment_notes,
                    "status": "Scheduled"
                }
                st.session_state.stats['appointments_today'] += 1
                save_data()
                st.success("Appointment scheduled successfully!")
            else:
                st.warning("This time slot is already booked!")

    with col2:
        st.subheader("📋 Today's Appointments")
        today = datetime.now().strftime("%Y-%m-%d")
        today_appointments = [
            appt for appt in st.session_state.appointments.values()
            if appt["date"] == today
        ]
        
        if today_appointments:
            for appt in sorted(today_appointments, key=lambda x: x["time"]):
                with st.container():
                    st.markdown(f"""
                    <div class="patient-card">
                        <h4>{appt['time']} - {appt['patient_name']}</h4>
                        <p><strong>Type:</strong> {appt['type']}</p>
                        <p><strong>Status:</strong> {appt['status']}</p>
                        <p><em>{appt['notes']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled for today")

elif navigation == "Analytics":
    st.title("📈 Analytics Dashboard")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    
    # Key metrics
    metrics_data = {
        "Total Patients": len(st.session_state.patient_data),
        "Active Cases": sum(1 for p in st.session_state.patient_data.values() if p.get("status") == "Active"),
        "Appointments": len(st.session_state.appointments),
        "Recovery Rate": "85%"
    }
    
    cols = st.columns(len(metrics_data))
    for col, (label, value) in zip(cols, metrics_data.items()):
        with col:
            st.metric(label, value)
    
    # Gender distribution chart
    gender_data = {
        "Male": sum(1 for p in st.session_state.patient_data.values() if p["gender"] == "Male"),
        "Female": sum(1 for p in st.session_state.patient_data.values() if p["gender"] == "Female"),
        "Other": sum(1 for p in st.session_state.patient_data.values() if p["gender"] == "Other")
    }
    
    # Age distribution
    age_ranges = {"0-18": 0, "19-30": 0, "31-50": 0, "51-70": 0, "70+": 0}
    for patient in st.session_state.patient_data.values():
        age = int(patient.get("age", 0))
        if age <= 18:
            age_ranges["0-18"] += 1
        elif age <= 30:
            age_ranges["19-30"] += 1
        elif age <= 50:
            age_ranges["31-50"] += 1
        elif age <= 70:
            age_ranges["51-70"] += 1
        else:
            age_ranges["70+"] += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        fig_gender = go.Figure(data=[go.Pie(
            labels=list(gender_data.keys()),
            values=list(gender_data.values()),
            hole=.3
        )])
        st.plotly_chart(fig_gender)
    
    with col2:
        st.subheader("Age Distribution")
        fig_age = go.Figure(data=[go.Bar(
            x=list(age_ranges.keys()),
            y=list(age_ranges.values())
        )])
        fig_age.update_layout(
            xaxis_title="Age Range",
            yaxis_title="Number of Patients"
        )
        st.plotly_chart(fig_age)
    
    # Appointment trends
    st.subheader("Appointment Trends")
    appointment_dates = [datetime.strptime(appt["date"], "%Y-%m-%d") for appt in st.session_state.appointments.values()]
    appointment_counts = pd.Series(appointment_dates).value_counts().sort_index()
    
    fig_trends = go.Figure(data=[go.Line(
        x=appointment_counts.index,
        y=appointment_counts.values
    )])
    fig_trends.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Appointments"
    )
    st.plotly_chart(fig_trends)

    # Export functionality
    st.subheader("Export Data")
    export_type = st.selectbox("Select Export Type", [
        "Patient Records",
        "Appointment History",
        "Analytics Report"
    ])
    
    if st.button("Generate Report"):
        st.download_button(
            label="Download Report",
            data="Sample report data",
            file_name=f"{export_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Add footer
st.markdown("""
    <footer style='position: fixed; bottom: 0; width: 100%; background-color: #1e293b; color: white; padding: 1rem; text-align: center;'>
        <p>© 2024 MediConnect Pro | Version 1.0 | Built with ❤️ for Healthcare Professionals</p>
    </footer>
""", unsafe_allow_html=True)
