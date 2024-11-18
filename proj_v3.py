# Function to make the output dictionary 
def make_output_dict(teams):
    students_sorted = {"tutorial_group": {}} # Initialize the main dictionary structure
    
    for group, team in teams:
        if group not in students_sorted["tutorial_group"]: # Ensure no duplucates for groups
            students_sorted["tutorial_group"][group] = {"teams": {}} # Add groups to dictionary
        
        # Generate a team ID (e.g., Team 1, Team 2, etc.)
        team_id = f"Team {len(students_sorted['tutorial_group'][group]['teams']) + 1}" # Use formatted string to asign team numbers
        
        # Add each student's details to the appropriate team
        students_sorted["tutorial_group"][group]["teams"][team_id] = {} # Initialise Dictionary for student's details
        for student in team:
            student_id = student['Student ID'] # Add student ID to dictionary
            students_sorted["tutorial_group"][group]["teams"][team_id][student_id] = { # Add Details to dictionary
                "School": student['School'],
                "Name": student['Name'],
                "Gender": student['Gender'],
                "CGPA": student['CGPA']
            }
    return students_sorted

# Function to print output dictionary in a readable and nice manner
def print_nested_dict(students_sorted_dict):
    for tutorial_group, tg_data in students_sorted_dict["tutorial_group"].items(): # Loop over the sub-dictionary for tutorial groups
        print(f"Tutorial Group: {tutorial_group}") # Use formatted string to print tutorial groups
        
        for team_id, team_data in tg_data["teams"].items(): # Loop over the sub-dictionary for teams
            print(f"  {team_id}:") # Use formatted string to print teams
            
            for student_id, details in team_data.items(): # Loop over the sub-dictionary for student id and details
                print(f"    Student ID: {student_id}") # Use formatted string to print student id
                for key, value in details.items(): # Loop over the sub-dictionary for student details
                    print(f"      {key}: {value}") # Use formatted string to print student detials
                print()  # Blank line between students for readability
            print("Diversity Score : ", score_calculation_check(teams,(1,1,1),4.15, True)) # Print diversity score for each team                
            print()  # Blank line between teams
        print()  # Blank line between tutorial groups

# Generate teams using the existing team creation functions
# teams = create_teams(students)

# Generate the nested dictionary output
students_sorted_dict = make_output_dict(teams)

# Display the resulting nested dictionary structure
print_nested_dict(students_sorted_dict)







