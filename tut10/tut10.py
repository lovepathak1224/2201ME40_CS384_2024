import sys
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# File paths
input_file_path = sys.argv[1]
output_file_generated_path = sys.argv[2]

try:
    # Load the input Excel file
    input_data = pd.read_excel(input_file_path, sheet_name='Sheet1')
    logging.info("Input file loaded successfully.")

    # Extract max marks and weightage rows
    max_marks = input_data.iloc[0, 2:6].values.astype(float)  # Max marks for each assessment
    weightage = input_data.iloc[1, 2:6].values.astype(float)  # Weightage for each assessment

    # Retain max marks and weightage rows as DataFrames for easy re-adding
    max_marks_row = pd.DataFrame([['', '', *max_marks]], columns=input_data.columns)
    weightage_row = pd.DataFrame([['', '', *weightage]], columns=input_data.columns)
    max_marks_row.iloc[0, 0] = 'Max Marks'
    weightage_row.iloc[0, 0] = 'Weightage'

    # Drop the first two rows to process student data
    student_data = input_data.iloc[2:].copy()

    # Identify assessment columns dynamically
    assessment_columns = student_data.columns[2:6]

    # Identify students with missing or non-numeric values in assessment columns
    missing_values = student_data[assessment_columns].apply(lambda x: x.map(lambda y: not isinstance(y, (int, float)) or pd.isna(y)))
    missing_students = student_data.loc[missing_values.any(axis=1), 'Roll']

    if not missing_students.empty:
        logging.warning("Missing values found in assessment scores for the following students:")
        for roll in missing_students:
            print(f"Roll Number with missing values in assessments: {roll}")

    # Calculate the weighted score for each student
    def calculate_total_weighted_score(row):
        try:
            scores = row[assessment_columns].values.astype(float)  # Scores for assessments
            weighted_scores = (weightage * scores) / max_marks
            total_score = np.sum(weighted_scores)
            return total_score
        except Exception as e:
            logging.error(f"Error calculating weighted score for Roll {row['Roll']}: {e}")
            return np.nan

    student_data['Total Scaled/100'] = student_data.apply(calculate_total_weighted_score, axis=1)

    # Sorting parameters and grades based on `old iapc record`
    total_students = len(student_data)
    iapc_record = {'AA': 5, 'AB': 15, 'BB': 25, 'BC': 30, 'CC': 15, 'CD': 5, 'DD': 5}  # Sample distribution
    grades = []

    # Calculate "Counts", "Round" for each grade, and include "Old IAPC Record"
    for grade, percentage in iapc_record.items():
        count = (percentage / 100) * total_students
        rounded_count = round(count)
        grades.append((grade, percentage, count, rounded_count))

    # Add additional grades with 0 counts and "Old IAPC Record"
    additional_grades = ['F', 'I', 'PP', 'NP']
    for grade in additional_grades:
        grades.append((grade, 0, 0, 0))

    # Assign grades to students based on sorted total scores
    student_data_sorted = student_data.sort_values(by='Total Scaled/100', ascending=False).reset_index(drop=True)
    grade_counts = {grade[0]: grade[3] for grade in grades if grade[3] > 0}  # Round off grade counts to distribute

    assigned_grades = []
    for grade, count in grade_counts.items():
        assigned_grades.extend([grade] * count)

    # Adjust the assigned grades to match the exact number of students
    total_needed_grades = len(student_data_sorted)
    if len(assigned_grades) > total_needed_grades:
        assigned_grades = assigned_grades[:total_needed_grades]  # truncate if excess
    elif len(assigned_grades) < total_needed_grades:
        assigned_grades.extend(['DD'] * (total_needed_grades - len(assigned_grades)))  # add 'DD' if short

    # Assign computed grades to sorted students
    student_data_sorted['Grade'] = assigned_grades

    # Sorting for each required sheet
    grade_sorted_sheet = student_data_sorted.copy()
    roll_sorted_sheet = student_data_sorted.sort_values(by='Roll').reset_index(drop=True)

    # Create Counts Summary as a separate section with "Old IAPC Record"
    counts_summary = pd.DataFrame(grades, columns=['Grade', 'Old IAPC Record (%)', 'Counts', 'Round'])
    counts_summary['Count Verified'] = counts_summary['Round']

    # Add a row for the total number of students
    counts_summary.loc[len(counts_summary)] = ['Total Students', '', total_students, '', '']

    # Save the result to an Excel file with the necessary sheets, including Max Marks, Weightage, and Counts Summary
    with pd.ExcelWriter(output_file_generated_path) as writer:
        # Write the grade-sorted sheet with Max Marks and Weightage rows
        pd.concat([max_marks_row, weightage_row, grade_sorted_sheet], ignore_index=True).to_excel(writer, sheet_name='Sheet1_Grade_Sorted', index=False)
        counts_summary.to_excel(writer, sheet_name='Sheet1_Grade_Sorted', index=False, startrow=len(grade_sorted_sheet) + 4)
        
        # Write the roll-sorted sheet with Max Marks and Weightage rows
        pd.concat([max_marks_row, weightage_row, roll_sorted_sheet], ignore_index=True).to_excel(writer, sheet_name='Sheet2_Roll_Sorted', index=False)
        counts_summary.to_excel(writer, sheet_name='Sheet2_Roll_Sorted', index=False, startrow=len(roll_sorted_sheet) + 4)

    logging.info("Output file generated successfully.")

except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
