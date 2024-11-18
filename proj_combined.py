import random

# parsing csv and loading student data
students = []  # list to hold all students' records

# read the csv file and store the student data in a list of dictionaries
with open('records.csv', 'r') as file:
    next(file)  # skip the header
    for line in file:
        # adjusting to the new column order: tutorial group, group, student id, school, name, gender, cgpa
        tutorial_group, student_id, school, name, gender, cgpa = line.strip().split(',')  # segregating by lines
        students.append({
            'Tutorial Group': tutorial_group,
            'Student ID': student_id,
            'Name': name,
            'School': school,
            'Gender': gender,
            'CGPA': float(cgpa),
            'Assigned Team': None  # placeholder for team assignment
        })

# function to calculate the average cgpa for a group
def calculate_average_cgpa(students):
    total_cgpa = sum(student['CGPA'] for student in students)
    return total_cgpa / len(students)

# function to find the best-fit student based on cgpa needs
def find_best_fit_student(students, target_cgpa, current_team_cgpa):
    best_fit = None
    smallest_difference = float('inf') #finds the lowest value in a list

    for student in students:
        # calculate new team CGPA if student is added
        new_team_cgpa = (current_team_cgpa + student['CGPA']) / (len(students) + 1)
        # calculate difference from target CGPA
        difference = abs(new_team_cgpa - target_cgpa)
        # select student with smallest difference from target CGPA
        if difference < smallest_difference:
            smallest_difference = difference
            best_fit = student

    return best_fit



############### NIGEL's I ADDED THIS #######################


def score_calculation(cur_group, score_weightage,target_cgpa,verbose = False):  # Score calculation for each group, the lower the better ,  0 is ideal (not possible due to 3 female, 2 male )
    count = 0
    #getting average amongst all students
    sum_group_gpa = sum([student['CGPA'] for student in cur_group])
    mean_gpa =  sum_group_gpa / len(cur_group)

    # calculate diversity for school count
    student_schools = set(student['School'] for student in cur_group)

    #gender diversity check
    gender_inc = 0
    for x in cur_group:
        if x['Gender'] == 'Male':
            gender_inc += 1
        else:
            gender_inc -= 1

    #generate all 3 scores

    #nigel i commented this code, just did a slight adjustment; please read the comments on the lines
    # gpa_score = abs(mean_gpa - target_cgpa) * score_weightage[0]
    # school_score = abs(len(cur_group) - len (student_schools)) * score_weightage[1]
    # gender_diversity_score =  abs (gender_inc * score_weightage[2])


    #here by ruri
    gpa_diff = abs(mean_gpa - target_cgpa)
    #(1 + gpa_diff) implemented so that as gpa_diff increases, this multiplier becomes larger, amplifying the impact of the CGPA difference on gpa_score
    #ff the group’s mean CGPA is very close to the target, gpa_diff is small, and the impact of gpa_score is minimal
    #if the group’s mean CGPA is far from the target, gpa_diff is larger, and this amplifies the weight of gpa_score
    gpa_score = gpa_diff * (1 + gpa_diff) * score_weightage[0]  # dynamically weighted by deviation
    school_score = abs(len(cur_group) - len(student_schools)) * score_weightage[1]
    gender_diversity_score = abs(gender_inc) * score_weightage[2]


    #give us a detailed output if the score has exceeded ideal (1)
    if (gender_diversity_score + gpa_score + school_score > 2 and verbose):
        print('The GPA: ',gpa_score)
        print('The Gender: ',gender_diversity_score)
        print('The School: ',school_score)
        print(cur_group)
        count += 1

    return gender_diversity_score + gpa_score + school_score


#function finding the "best" student to fit, based on our score calculator
def find_best_fit_score(students,target_cgpa,cur_team):
    best_fit = None
    smallest_difference = float('inf')

    for student in students:
        # calculate score if student is added
        cur_score =  score_calculation(cur_team + [student],(1,1,1),target_cgpa)
        # choose student with smallest score difference
        if (cur_score < smallest_difference):
            smallest_difference = cur_score
            best_fit = student
    return best_fit


############### NIGEL's #######################

# function to form a single team
def form_team(students, target_cgpa):
    team = []

    # step 1: selecting highest and lowest cgpa students
    students.sort(key=lambda x: x['CGPA'])
    lowest_cgpa_student = students[0]
    highest_cgpa_student = students[-1]

    # append selected students from the pool
    team.append(lowest_cgpa_student)
    team.append(highest_cgpa_student)

    # remove selected students from the pool
    students.remove(lowest_cgpa_student)
    students.remove(highest_cgpa_student)

    # current team's cgpa
    current_team_cgpa = sum(student['CGPA'] for student in team)


    # step 2: add students to the team using "best fit" method to balance cgpa
    # Ruri, I suggest this , your code above is commented out; ruri: accepted!
    # The team currently has highest CGPA student and lowest CGPA student
    while len(team) < 5:
        best_fit_student = find_best_fit_score(students,target_cgpa, team)
        team.append(best_fit_student) #append in the best fit student
        students.remove(best_fit_student) #remove him from the available pool



    # After getting the best student by score based on CGPA, Gender and School

    # step 3: check gender balance (3:2 ratio)
    males = [student for student in team if student['Gender'] == 'Male']
    females = [student for student in team if student['Gender'] == 'Female']

    # ensure 3 males, 2 females or vice versa
    if len(males) > 3:
        to_remove = random.choice(males)
        team.remove(to_remove)
        students.append(to_remove)
        available_females = [s for s in students if s['Gender'] == 'Female']
        if available_females:  # check if there are any females available
            replacement = random.choice(available_females)
            team.append(replacement)
            students.remove(replacement)
    elif len(females) > 3:
        to_remove = random.choice(females)
        team.remove(to_remove)
        students.append(to_remove)
        available_males = [s for s in students if s['Gender'] == 'Male']
        if available_males:  # check if there are any males available
            replacement = random.choice(available_males)
            team.append(replacement)
            students.remove(replacement)


    # step 4: check school diversity (at least 3 schools)
    schools = {student['School'] for student in team}
    if len(schools) < 3:
        # try swapping students to achieve school diversity
        potential_swaps = [s for s in team if team.count(s['School']) > 1]

        if potential_swaps:  # check if there are any eligible students for swapping
            to_swap = random.choice(potential_swaps)
            for student in students:
                if student['School'] not in schools:
                    team.remove(to_swap)
                    students.append(to_swap)
                    team.append(student)
                    students.remove(student)
                    schools.add(student['School'])
                    if len(schools) >= 3:
                        break

    return team

# function to create teams for each tutorial group
def create_teams(students):
    tutorial_groups = {}
    teams = []

    # separate students by tutorial group
    for student in students:
        group = student['Tutorial Group']
        if group not in tutorial_groups:
            tutorial_groups[group] = []
        tutorial_groups[group].append(student)

    # form teams for each tutorial group
    for group, group_students in tutorial_groups.items():
        target_cgpa = calculate_average_cgpa(group_students)

        # continue forming teams until fewer than 5 students are left
        while len(group_students) >= 5:
            team = form_team(group_students, target_cgpa)
            teams.append((group, team))

    return teams

# generate teams
teams = create_teams(students)

#display teams
# for i, (group, team) in enumerate(teams, start=1):
#     print(f"Team {i} (Group {group}):")
#     for student in team:
#         print(f"  {student['Name']} (CGPA: {student['CGPA']}, School: {student['School']}, Gender: {student['Gender']})")
#         #print out diversity together
#     print("Diversity Score : ", score_calculation(team,(1,1,1),4.15, True))

#     print()

## Insert Code here

# Score calculation for each group, the lower the better ,  0 is ideal (not possible due to 3 female, 2 male )
def score_calculation_check(cur_group, score_weightage,target_mean = 4.15,verbose = False):  
    sum_group_gpa = sum([student['CGPA'] for student in cur_group])  
    mean_gpa =  sum_group_gpa / len(cur_group) #getting average amongst all students


    gender_inc = 0

    student_schools = set(student['School'] for student in cur_group)
    for x in cur_group:
        if x['Gender'] == 'Male':
            gender_inc += 1
        else:
            gender_inc -= 1

    gpa_score = abs (mean_gpa - target_mean) * score_weightage[0]
    school_score = abs(len(cur_group) - len (student_schools)) * score_weightage[1]
    gender_diversity_score =  abs (gender_inc * score_weightage[2])
    if (gender_diversity_score + gpa_score + school_score > 2 and verbose):
        print('GPA Score : ',gpa_score)
        print('Gender Score : ',gender_diversity_score)
        print('School Score : ',school_score)
        print(cur_group)

    return  gender_diversity_score + gpa_score + school_score

# display teams
# for i, (group, team) in enumerate(teams, start=1):
#     print(f"Team {i} (Group {group}):")
#     print("Diversity Score : ", score_calculation_check(team,(1,1,1),4.15, True))

#     print()

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

# Generate the nested dictionary output
students_sorted_dict = make_output_dict(teams)

# Display the resulting nested dictionary structure
print_nested_dict(students_sorted_dict)