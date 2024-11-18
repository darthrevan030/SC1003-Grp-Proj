#nested dictionaries to hold all the individual TG
students = {"tutorial_group":{
                "teams":{
                    "student_id":{
                        "student_details":{
                        "School":"placeholder_school",
                        "Name":"placeholder_name",
                        "Gender":"placeholder_gender",
                        "CGPA":"placeholder_cgpa"}
                                }
                        }
                            }
            }

#alias the dictionary levels for easier referencing later
students_tutorial_group_dict = students['tutorial_group']
students_tg_sub_dict = students['tutorial_group']["tg_sub"]
students_student_id_dict = students['tutorial_group']["tg_sub"]["student_id"]
students_student_details_dict = students['tutorial_group']["tg_sub"]["student_id"]["student_details"]

#read the CSV file and store the student data in a nested dictionary data structure as shown above
tutorial_groups = []
student_ids = []
names = []
schools = []
genders = []
cgpas = []



with open('records.csv', 'r') as file:
    next(file)  # skip the header
    for line in file:
        tutorial_group, student_id, school, name, gender, cgpa = line.strip().split(',') #segregating by lines
        if tutorial_group not in tutorial_groups: #add tutorial groups into 1 list
            tutorial_groups.append(tutorial_group)
        sorted_tutorial_groups = tutorial_groups.sort()
        if student_id not in student_ids:
            student_ids.append(student_id) #add student ids into 1 list    
        names.append(name) #add names into 1 list 
        schools.append(school) #add schools into 1 list
        genders.append(gender) #add students genders into 1 list
        cgpas.append(cgpa) #add students cgpa into 1 list

for item in tutorial_groups:
    students["tutorial_group"] = {sorted_tutorial_groups:"placeholder_tg_sub"}


# for std_id in student_ids:
#     students["tutorial_group"]["tg_sub"]["student_id"] = student_ids



#print(students)

# print(tutorial_groups)
# print(len(tutorial_groups))

# print(student_ids)
# print(len(student_ids))

# print(names)
# print(len(names))

# print(schools)
# print(len(schools))

# print(genders)
# print(len(genders))

# print(cgpas)
# print(len(cgpas))