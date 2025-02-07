import streamlit as st
import subprocess
import os
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Report Processing & Visualization App")

# Upload executive report
exec_file = st.sidebar.file_uploader("Upload Executive Report (Excel)", type=["xlsx"])
journey_file = st.sidebar.file_uploader("Upload Journey Report (CSV)", type=["csv"])

# ✅ Initialize session state for download button and visualization
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False

if st.sidebar.button("Process Reports"):
    if exec_file and journey_file:
        # Clear previous state
        st.session_state.processing_done = False  

        with open("./temp/missing_courses.txt", "w") as f:
            f.write("")  # Clear old warnings

        # Run processing scripts
        try:
            subprocess.run(["python3", "scripts/report_cleanup.py"], check=True)
            subprocess.run(["python3", "scripts/report_update.py"], check=True)
            st.sidebar.success("✅ Processing complete!")
            st.session_state.processing_done = True  # ✅ Mark processing as done
        except subprocess.CalledProcessError as e:
            st.sidebar.error(f"❌ Error running scripts: {e}")

        # Read missing courses and display warning
        if os.path.exists("./temp/missing_courses.txt"):
            with open("./temp/missing_courses.txt", "r") as f:
                missing_courses = f.readlines()
            
            if missing_courses:
                st.warning("⚠️ The following course reports were missing and skipped:")
                for course in missing_courses:
                    st.write(f"- {course.strip()}")  # Display each missing course

# ✅ **Show the Download Button ONLY After Processing**
report_path = "./reports/updated_executive_report.csv"

if st.session_state.processing_done and os.path.exists(report_path):
    st.success("✅ Processing complete! Download your updated report below:")
    
    with open(report_path, "rb") as f:
        st.download_button("📥 Download Updated Report", f, file_name="updated_executive_report.csv")

    # ✅ **Step 2: Load Processed Data for Visualization**
    df = pd.read_csv(report_path)

    # ✅ **Show Data Preview**
    st.write("### 📋 Processed Report Preview")
    st.dataframe(df.head(20))  # Show first 20 rows

    # ✅ **Step 3: Create Visualizations**
    st.write("### 📊 Data Visualizations")

    # **Completion Rate Per Course**
    completion_counts = df.apply(lambda col: (col == "Completed").sum() if col.dtype == "object" else 0)
    completion_counts = completion_counts[completion_counts > 0]  # Only keep columns with "Completed" values

    if not completion_counts.empty:
        st.write("#### ✅ Completion Rates per Course")
        fig, ax = plt.subplots(figsize=(10, 5))
        completion_counts.plot(kind="bar", ax=ax)
        plt.xticks(rotation=45)
        plt.ylabel("Number of Completions")
        plt.xlabel("Course")
        plt.title("Completion Rates per Course")
        st.pyplot(fig)
    else:
        st.info("No completion data available for visualization.")

    # **Overall Status Breakdown (Pie Chart)**
    st.write("#### 📌 Completion vs. Incomplete Breakdown")
    total_completed = (df == "Completed").sum().sum()
    total_incomplete = df.shape[0] * (df.shape[1] - 1) - total_completed  # Estimate of incomplete statuses

    if total_completed > 0:
        fig, ax = plt.subplots()
        ax.pie([total_completed, total_incomplete], labels=["Completed", "Incomplete"], autopct="%1.1f%%", startangle=90)
        ax.set_title("Overall Training Status Breakdown")
        st.pyplot(fig)
    else:
        st.info("No completion data found for pie chart.")
