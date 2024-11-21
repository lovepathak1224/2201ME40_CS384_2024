from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import tempfile
import datetime as dt

app = Flask(__name__)

temp_dir = tempfile.TemporaryDirectory()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Getting user inputs for buffer and seating option
    buffer = int(request.form['buffer'])
    sparse_option = request.form['seating']
    sparse = sparse_option == 'sparse'

    # Reading the uploaded files
    students_file = request.files['students_file']
    schedule_file = request.files['schedule_file']
    rooms_file = request.files['rooms_file']



    # Save uploaded files in the temp directory
    students_path = os.path.join(temp_dir.name, 'students.csv')
    schedule_path = os.path.join(temp_dir.name, 'schedule.csv')
    rooms_path = os.path.join(temp_dir.name, 'rooms.csv')


    students_file.save(students_path)
    schedule_file.save(schedule_path)
    rooms_file.save(rooms_path)

    # Load dataframes
    students_df = pd.read_csv(students_path, skiprows=1)
    schedule_df = pd.read_csv(schedule_path, skiprows=1)
    rooms_df = pd.read_csv(rooms_path)

    # Parsing Morning and Evening courses
    schedule_df['Morning Courses'] = schedule_df['Morning'].apply(lambda x: x.split('; ') if pd.notna(x) else [])
    schedule_df['Evening Courses'] = schedule_df['Evening'].apply(lambda x: x.split('; ') if pd.notna(x) else [])

    # Logic for seating arrangement
    def assign_rooms(courses, rooms_df, buffer, sparse):
        assignments = []
        room_capacity_left = rooms_df[['Room No.', 'Exam Capacity']].copy()
        room_capacity_left['Remaining Capacity'] = room_capacity_left['Exam Capacity'] - buffer

        for course in courses:
            students = students_df[students_df['course_code'] == course]['rollno'].tolist()
            num_students = len(students)

            for _, room in room_capacity_left.iterrows():
                if room['Remaining Capacity'] <= 0:
                    continue
                
                max_students_in_room = min(room['Remaining Capacity'], num_students)
                if sparse:
                    max_students_in_room = min(max_students_in_room, room['Exam Capacity'] // 2)
                
                assigned_students = max_students_in_room
                assigned_roll_numbers = students[:assigned_students]
                students = students[assigned_students:]
                num_students -= assigned_students
                
                room_capacity_left.loc[room_capacity_left['Room No.'] == room['Room No.'], 'Remaining Capacity'] -= assigned_students

                existing_assignment = next((a for a in assignments if a['Room'] == room['Room No.']), None)
                if existing_assignment:
                    existing_assignment['Courses'] += f", {course}"
                    existing_assignment['Roll Numbers'] += f", {', '.join(assigned_roll_numbers)}"
                    existing_assignment['Students Assigned'] += assigned_students
                    existing_assignment['Vacant Seats'] = room_capacity_left.loc[room_capacity_left['Room No.'] == room['Room No.'], 'Remaining Capacity'].values[0]
                else:
                    assignments.append({
                        'Room': room['Room No.'],
                        'Block': rooms_df.loc[rooms_df['Room No.'] == room['Room No.'], 'Block'].values[0],
                        'Courses': course,
                        'Students Assigned': assigned_students,
                        'Vacant Seats': room_capacity_left.loc[room_capacity_left['Room No.'] == room['Room No.'], 'Remaining Capacity'].values[0],
                        'Roll Numbers': ', '.join(assigned_roll_numbers),
                        'Buffer Seats': buffer  # Add Buffer Seats to each room
                    })
                
                if num_students == 0:
                    break
            
            if num_students > 0:
                print(f"Warning: Not enough rooms for course {course} with {num_students} students remaining.")
        
        return assignments

    output = []
    for _, row in schedule_df.iterrows():
        date = row['Date']
        day = row['Day']

        morning_assignments = assign_rooms(row['Morning Courses'], rooms_df, buffer, sparse)
        for assignment in morning_assignments:
            output.append({
                'Date': date,
                'Day': day,
                'Session': 'Morning',
                'Room': assignment['Room'],
                'Block': assignment['Block'],
                'Courses': assignment['Courses'],
                'Students Assigned': assignment['Students Assigned'],
                'Vacant Seats': assignment['Vacant Seats'],
                'Buffer Seats': assignment['Buffer Seats'],  # Include buffer seats in output
                'Roll Numbers': assignment['Roll Numbers']
                
            })
        
        evening_assignments = assign_rooms(row['Evening Courses'], rooms_df, buffer, sparse)
        for assignment in evening_assignments:
            output.append({
                'Date': date,
                'Day': day,
                'Session': 'Evening',
                'Room': assignment['Room'],
                'Block': assignment['Block'],
                'Courses': assignment['Courses'],
                'Students Assigned': assignment['Students Assigned'],
                'Vacant Seats': assignment['Vacant Seats'],
                'Buffer Seats': assignment['Buffer Seats'],
                'Roll Numbers': assignment['Roll Numbers']
            })

    # Save to CSV
    output_df = pd.DataFrame(output)
    output_csv = os.path.join(temp_dir.name, 'seating_arrangement_final.csv')
    output_df.to_csv(output_csv, index=False)

    # Render output page with results
    return render_template('output.html', tables=[output_df.to_html(classes='data', index=False)], output_csv=output_csv)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(temp_dir.name, filename)
    return send_file(file_path, as_attachment=True)


@app.route('/generate_attendance', methods=['POST'])
def generate_attendance():
    try:
        date = request.form['date']
        room_no = request.form['room_no']
        shift = request.form['Shift']
        seating_file = request.files['seating_file']
        student_file = request.files['student_file']

        # Save uploaded files in the temp directory
        seating_path = os.path.join(temp_dir.name, 'seating.csv')
        student_path = os.path.join(temp_dir.name, 'students.csv')
        
        seating_file.save(seating_path)
        student_file.save(student_path)

        seating_data = pd.read_csv(seating_path)
        student_data = pd.read_csv(student_path)

        # Clean and filter the seating data
        seating_data['Date'] = seating_data['Date'].str.strip()
        seating_data['Room'] = seating_data['Room'].astype(str).str.strip()
        seating_data['Session'] = seating_data['Session'].str.strip()

        filtered_seating = seating_data[
            (seating_data['Date'] == date) &
            (seating_data['Room'] == room_no) &
            (seating_data['Session'] == shift)
        ]

        if filtered_seating.empty:
            return "No data found for the given date and room."
        
        # Extract roll numbers and map to names
        roll_numbers = filtered_seating['Roll Numbers'].dropna().str.split(',').explode()
        roll_numbers = roll_numbers.str.strip()
        roll_no = roll_numbers.tolist()

        roll_name_mapping = dict(zip(student_data['Roll'], student_data['Name']))

        # Prepare attendance data
        attendance_data = []
        for roll in roll_no:
            name = roll_name_mapping.get(roll, 'Name Not Found')
            attendance_data.append({'Roll Number': roll, 'Name': name})

        attendance_df = pd.DataFrame(attendance_data)
        attendance_df['Signature'] = ""

        # Add blank rows for signatures
        blank_rows = pd.DataFrame([["","",""],["", "Invigilator 1", ""],["", "Invigilator 2", ""],["", "TA 1", ""],["", "TA 2", ""],["", "TA 3", ""]], columns=attendance_df.columns)
        
        attendance_df = pd.concat([attendance_df, blank_rows], ignore_index=True)

        metadata = pd.DataFrame({
            'Room No': [room_no],
            'Shift': [shift],
            'Date': [date]
        })

        
        # Save attendance CSV in the temp directory
        output_csv = os.path.join(temp_dir.name, 'attendance_sheet.csv')

        with open(output_csv, mode='w', newline='') as f:
            metadata.to_csv(f, header=True, index=False)
            attendance_df.to_csv(f, header=True, index=False)
        return render_template('output2.html',title=f'Attendance Sheet',date=date, room_no=room_no,shift=shift,tables=[attendance_df.to_html(classes='data', index=False)], output_csv=output_csv)
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)