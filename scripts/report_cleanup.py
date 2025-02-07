import pandas as pd
import os

# Step 1: Convert the executive report from XLSX to CSV
excel_file_path = './executive_reports/executive_report.xlsx'
csv_file_path = './temp/executive_report.csv'  
df_excel = pd.read_excel(excel_file_path)
df_excel.to_csv(csv_file_path, index=False)

print("2+1 executive report converted to CSV.")

# Step 2: Reorder columns and save as CSV
file_path = './journeyUserSummaryV2 Report.csv'
df = pd.read_csv(file_path)

# Move 'USER ID' and 'JOURNEY STATUS' columns to the front
columns_to_move = ['USER ID', 'JOURNEY STATUS']

if all(col in df.columns for col in columns_to_move):
    other_columns = [col for col in df.columns if col not in columns_to_move]
    new_column_order = columns_to_move + other_columns
    df = df[new_column_order]

# Save the reordered columns to a CSV file
reordered_file_path = './temp/reordered_columns.csv'
df.to_csv(reordered_file_path, index=False)

print("2+1 report clean up is ongoing...")

# Step 3: Filter for BD team courses and save as separate CSVs
data = pd.read_csv(reordered_file_path)

course_groups = {
    'AI 101': ['Artificial Intelligence for Associates 101', 'Artificial Intelligence For Executive Leaders', 'Artificial Intelligence for Leaders', 'Artificial Intelligence for Practitioners'],
    'HCD 101': ['Human Centered Design For Leaders', 'Human Centered Design For Professionals', 'Human Centred Design For Associates (101)', 'Human Centred Design For Practitioners'],
    'Data Analytics 101':['Big Data & Analytics for Leaders','Big Data & Analytics for Practitioners','Big Data & Analytics for Professionals','Data Analytics for Associates (101)'],
    'Cloud 101' : ['Cloud Computing for Associates (101)','Cloud Computing for Leaders','Cloud Computing for Practitioners','Cloud Computing for Professionals'],
    'Cyber Security 101' : ['Cyber Security for Associate (101)','Cyber Security for Executive Leaders','Cyber Security for Practitioners','Cyber Security Professionals','Cyber Security Specialists'],
    'FinTech' : ['Fintech For Associate (101)', 'Fintech for leaders'],
    'RPA':['Robotic Process Automation for Associates','Robotic Process Automation for Leaders','Robotic Process Automation for Practitioners','Robotic Process Automation for Professionals'],
    'Machine Learning' : ['Machine Learning For Associates (101)','Machine Learning For Leaders','Machine Learning For Practitioners','Machine Learning For Professionals'],
    'Agile': ['Agile for Associates (101)','Agile for Leaders','Agile for Practitioners'],
    'Programming 101' : ['Java Programming 101','Java Programming 102','Java Programming 103','Java Programming 104','Java Programming 105: Expert','Python Programming 101','Python Programming 102','Python Programming 103','Python Programming 104','Python Programming 105: Expert'],
    'Agile Project Management' : ['Agile Project Management 101'],
    'Care Academy' : ['Care Academy for Associates 101'],
    'Commercial Management' : ['Commercial Management 101'],
    'Business Process Modelling' : ['Business Process Modelling 101'],
    'Business Communication': ['Business Communication & Critical Business Thinking 101'],
    'Digital Product Mngt' : ['Digital Product Management 101'],
    'Crisis Management 101' : ['Crisis Management 101'],
    'Carbon Markets 101': ['Carbon Markets 101'],
    'Data Management 101': ['Data Management 101'],
    'Software Engineering 101' : ['Software Engineering for Associates','Software Engineering for Leaders','Software Engineering for Practitioners','Software Enginering for Professionals'],
    'IFRS (International Financial Reporting Standards)' : ['IFRS(International Financial Reporting Standards)'],
    'AI Governance' : ['AI Governance']
}

# Create a temp directory for the course files if it doesn't exist
os.makedirs('./temp/courses', exist_ok=True)

for group_name, courses in course_groups.items():
    group_data = data[data['JOURNEY TITLE'].isin(courses)]
    
    if not group_data.empty:
        group_file_path = f'./temp/courses/{group_name}.csv'
        group_data.to_csv(group_file_path, index=False)
        print(f"{group_name} data saved to {group_file_path}")

if group_data.empty:
    print(f"⚠️ Warning: {group_name} has no data. Creating an empty file to prevent errors.")


print("Course filtering and updating complete.")

# Step 4: Remove duplicates for each course and save cleaned data as CSV
output_directory = './cleaned/'
os.makedirs(output_directory, exist_ok=True)

status_priority = {'Completed': 1, 'started': 2}

for group_name in course_groups.keys():
    input_file_path = f'./temp/{group_name}.csv'
    
    if os.path.exists(input_file_path):
        df = pd.read_csv(input_file_path)

        # Check if 'JOURNEY STATUS' column exists
        if 'JOURNEY STATUS' in df.columns:
            df['Priority'] = df['JOURNEY STATUS'].map(status_priority)
            df = df.sort_values(by=['USER ID', 'Priority'])
            
            # Drop duplicates based on 'USER ID', keeping the highest priority (Completed)
            df = df.drop_duplicates(subset='USER ID', keep='first')
            
            # Drop the Priority column
            df = df.drop(columns=['Priority'])
        
        # Save the cleaned data back as CSV
        cleaned_file_path = f'{output_directory}/{group_name}_cleaned.csv'
        df.to_csv(cleaned_file_path, index=False)
        print(f"BD cleaned data saved to '{cleaned_file_path}'")
