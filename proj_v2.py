import csv

# Initialize the main dictionary structure
students_sorted = {}

# Read the CSV file and store the student data in a nested dictionary structure
with open('records.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    
    for line in csv_reader:
        tutorial_group, team, student_id, school, name, gender, cgpa = line
        
        # Create nested structure for tutorial group if it does not exist
        if tutorial_group not in students_sorted:
            students_sorted[tutorial_group] = {}

        # Create nested structure for team within the tutorial group if it does not exist
        if team not in students_sorted[tutorial_group]:
            students_sorted[tutorial_group][team] = {}
        
        # Add the student's details under the team and student ID
        students_sorted[tutorial_group][team][student_id] = {
            "School": school,
            "Name": name,
            "Gender": gender,
            "CGPA": cgpa
        }

# Display the resulting nested dictionary structure
print(students_sorted)
