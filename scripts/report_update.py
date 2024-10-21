import pandas as pd
import os

# Load the executive report
exec_report_path = './temp/executive_report.csv'
exec_report_df = pd.read_csv(exec_report_path)

# Define course files and their corresponding columns
course_columns = {
    './temp/courses/AI 101.csv' : 'AI 101',
    './temp/courses/HCD 101.csv' : 'HCD 101',
    './temp/courses/Data Analytics 101.csv' : 'Data Analytics 101',
    './temp/courses/Cloud 101.csv' : 'Cloud 101',
    './temp/courses/Cyber Security 101.csv' : 'Cyber Security 101',
    './temp/courses/FinTech.csv' : 'FinTech',
    './temp/courses/RPA.csv' : 'RPA',
    './temp/courses/Machine Learning.csv' : 'Machine Learning',
    './temp/courses/Agile.csv' : 'Agile',
    './temp/courses/Programming 101.csv' : 'Programming 101',
    './temp/courses/Agile Project Management.csv' : 'Agile Project Management',
    './temp/courses/Care Academy.csv' : 'Care Academy',
    './temp/courses/Commercial Management.csv' : 'Commercial Management',
    './temp/courses/Business Process Modelling.csv' : 'Business Process Modelling',
    './temp/courses/Business Communication.csv' : 'Business Communication',
    './temp/courses/Digital Product Mngt.csv' : 'Digital Product Mngt',
    './temp/courses/Crisis Management 101.csv' : 'Crisis Management 101',
    './temp/courses/Carbon Markets 101.csv' : 'Carbon Markets 101',
    './temp/courses/Data Management 101.csv' : 'Data Management 101',
    './temp/courses/Software Engineering 101.csv' : 'Software Engineering 101',
    './temp/courses/IFRS (International Financial Reporting Standards).csv' : 'IFRS (International Financial Reporting Standards)',
    './temp/courses/AI Governance.csv' : 'AI Governance',
}

# Iterate through each course file
for course_file, report_column in course_columns.items():
    course_df = pd.read_csv(course_file)

    # Step 5: Update the executive report
    for idx, row in course_df.iterrows():
        user_email = row['USER ID']
        journey_status = row['JOURNEY STATUS']

        # If the user is in the executive report
        if user_email in exec_report_df['Employee Email'].values:
            user_index = exec_report_df.index[exec_report_df['Employee Email'] == user_email][0]
            
            # Update if the status is 'Completed'
            if journey_status == 'Completed' and exec_report_df.at[user_index, report_column] != 'Completed':
                exec_report_df.at[user_index, report_column] = 'Completed'
        else:
            # Mark as 'Not Started' if user is not in the cleaned data
            if user_email in exec_report_df['Employee Email'].values:
                user_index = exec_report_df.index[exec_report_df['Employee Email'] == user_email][0]
                exec_report_df.at[user_index, report_column] = 'Not Started'

# Save the updated executive report
exec_report_df.to_csv('./reports/updated_executive_report.csv', index=False)
