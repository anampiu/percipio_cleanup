import pandas as pd

file_path =  './data.csv'
df = pd.read_csv(file_path)

#Moving vlookup colums to the first and second
columns_to_move = ['USER ID','JOURNEY STATUS']

if all(col in df.columns for col in columns_to_move):

    other_columns = [col for col in df. columns if col not in  columns_to_move]
    new_column_order = columns_to_move + other_columns
    df = df[new_column_order]
df.to_csv('ebu_reordered_colums.csv', index=False)

print("Columns have be reorderd and Clean up is ongoing...")

#Filter for FS team courses
data = pd.read_csv('./ebu_reordered_colums.csv')

course_groups = {
    'AI':['Artificial Intelligence for Associates 101','Artificial Intelligence For Executive Leaders','Artificial Intelligence for Leaders','Artificial Intelligence for Practitioners'],
    'Data Analytics':['Big Data & Analytics for Leaders','Big Data & Analytics for Practitioners','Big Data & Analytics for Professionals','Data Analytics for Associates (101)'],
    'Commercial Management': ['Commercial Management 101'],
}
with pd.ExcelWriter('ebu_remove_duplicates.xlsx') as writer:
    sheet_written = False

    for group_name, courses in course_groups.items():
        group_data = data[data['JOURNEY TITLE'].isin(courses)]
        if not group_data.empty:
            group_data.to_excel(writer, sheet_name=group_name, index=False)
            sheet_written = True
    
    if not sheet_written:
        raise ValueError("No data was written to any sheets, check your filtering logic.")
    
print("The Enterprise Business Unit team report is almost ready...")

# Remove duplicates for the team
file_path = './ebu_remove_duplicates.xlsx'  # Path to your Excel file
excel_data = pd.read_excel(file_path, sheet_name=None)  

output_file_path = './cleaned/EBU_cleaned_data.xlsx' 
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    # Process each sheet
    for sheet_name, df in excel_data.items():
        print(f"Processing sheet: {sheet_name}")
        
        status_priority = {'Completed': 1, 'started': 2}
        # Check if 'Status' column exists, change to journey status in caps
        if 'JOURNEY STATUS' in df.columns:
            df['Priority'] = df['JOURNEY STATUS'].map(status_priority)
            df = df.sort_values(by=['USER ID', 'Priority'])
            
            # Drop duplicates, keeping the first entry for each email (which has the highest priority)
            df = df.drop_duplicates(subset='USER ID', keep='first')
            
            # Drop the Priority column as it's no longer needed
            df = df.drop(columns=['Priority'])
        
        # Write the processed DataFrame to the new Excel file
        df.to_excel(writer, index=False, sheet_name=sheet_name)  # Write each DataFrame to a separate sheet

print(f"Cleaned data saved as '{output_file_path}'")