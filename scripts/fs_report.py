import pandas as pd
import os

# Load the executive report
exec_report_path = './temp/fs_executive_report.csv'
exec_report_df = pd.read_csv(exec_report_path)

# Strip whitespace from column names
exec_report_df.columns = exec_report_df.columns.str.strip()

# Define course files and their corresponding columns
course_columns = {
    './temp/fs_courses/AI.csv': 'AI 101',
    './temp/fs_courses/Data Analytics.csv': 'Data Analytics 101',
    './temp/fs_courses/RPA.csv': 'RPA',
    './temp/fs_courses/ML.csv': 'Machine Learning ',
    './temp/fs_courses/Programming.csv': 'Programming',
    './temp/fs_courses/HCD.csv': 'Human Centred Design',
    './temp/fs_courses/Business Process Modelling.csv': 'Business Process Modelling',
    './temp/fs_courses/Digital Product Management.csv': 'Digital Product Management',
    './temp/fs_courses/Digital Lending.csv': 'Digital Credit',
    './temp/fs_courses/Commercial Management.csv': 'Commercial Management',
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
exec_report_df.to_csv('./reports/fs_updated_executive_report.csv', index=False)
