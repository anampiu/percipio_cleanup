import streamlit as st
import pandas as pd
import os
import shutil
import subprocess

# Title of the app
st.title("📊 Report Processing App")

# Upload the executive report
st.sidebar.header("Upload Files")
exec_file = st.sidebar.file_uploader("Upload Executive Report (Excel)", type=["xlsx"])
journey_file = st.sidebar.file_uploader("Upload Journey Report (CSV)", type=["csv"])

# Temporary directories for processing
temp_dir = "./temp"
cleaned_dir = "./cleaned"
reports_dir = "./reports"

# Function to clean old files and prepare directories
def setup_directories():
    for folder in [temp_dir, cleaned_dir, reports_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

# Process the files when user clicks the button
if st.sidebar.button("Process Reports"):
    if exec_file and journey_file:
        setup_directories()

        # Save uploaded files
        exec_path = os.path.join(temp_dir, "executive_report.xlsx")
        journey_path = os.path.join(temp_dir, "journeyUserSummaryV2 Report.csv")
        
        with open(exec_path, "wb") as f:
            f.write(exec_file.getbuffer())
        
        with open(journey_path, "wb") as f:
            f.write(journey_file.getbuffer())

        st.sidebar.success("Files uploaded successfully! Processing now...")

        # Run the cleanup and update scripts
        try:
            subprocess.run(["python3", "report_cleanup.py"], check=True)
            subprocess.run(["python3", "report_update.py"], check=True)
            st.sidebar.success("Processing complete! Download your report below.")
        except subprocess.CalledProcessError as e:
            st.sidebar.error(f"Error running scripts: {e}")

# Show results if processing is complete
if os.path.exists(os.path.join(reports_dir, "updated_executive_report.csv")):
    st.write("✅ **Processing Complete!** Download your updated report below.")
    
    with open(os.path.join(reports_dir, "updated_executive_report.csv"), "rb") as f:
        st.download_button("📥 Download Updated Report", f, "updated_executive_report.csv")

