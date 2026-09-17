import mysql.connector
import matplotlib.pyplot as plt

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vansh",
    
)

cursor = db.cursor()

def create_tables():
    
    #Create Database if not exist
    cursor.execute("Create Database IF NOT EXISTS 1Project")
    cursor.execute("Use Project")
    db.commit()
    # Create a table to store user information
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
    db.commit()

    # Create a table to store questions for career recommendation
    cursor.execute("CREATE TABLE IF NOT EXISTS carrer_questionss (id INT AUTO_INCREMENT PRIMARY KEY, question_text VARCHAR(255))")
    db.commit()

    # Create a table to store user answers
    cursor.execute("CREATE TABLE IF NOT EXISTS user_answers (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, answer VARCHAR(255), FOREIGN KEY (user_id) REFERENCES users(id))")
    db.commit()
   
    # Create a table to store logic questions
    cursor.execute("CREATE TABLE IF NOT EXISTS logic_questions (id INT AUTO_INCREMENT PRIMARY KEY, question_text VARCHAR(255))")
    db.commit()
   
    #Create a table to store logic questions answers
    cursor.execute("CREATE TABLE IF NOT EXISTS logic_answers(id INT AUTO_INCREMENT PRIMARY KEY, answers VARCHAR(255))")
    
    test_questions = [
        "Do you enjoy working with numbers? (yes/no): ",
        "Are you interested in technology and computers? (yes/no): ",
        "Do you enjoy helping others? (yes/no): ",
        "Are you creative and enjoy expressing yourself? (yes/no): ",
        "Are you comfortable taking on leadership roles and making decisions for a group? (yes/no): ",
        "Do you enjoy exploring and understanding how things work in the natural world? (yes/no): ",
        "Are you good at organizing and planning events or activities? (yes/no): ",
        "Do you have a strong interest in business and entrepreneurship? (yes/no): ",
        "Are you comfortable speaking in front of a group of people? (yes/no): ",
        "Do you enjoy solving complex problems and puzzles(yes/no): ",
        "Are you comfortable working with deadlines and handling time-sensitive tasks?(yes/no): ",
        "Do you find joy in helping others understand new concepts or skills?(yes/no): ",
        "Are you interested in environmental sustainability and conservation efforts?(yes/no): ",
        "Do you enjoy analyzing and interpreting data to make informed decisions?(yes/no): ",
        "Are you interested in staying updated on the latest advancements in technology?(yes/no): ",
        "Are you interested in exploring different cultures and working in diverse environments?(yes/no): ",
        "Do you prefer a structured and organized work environment?(yes/no): "
    ]
   
    
    logic_questions = [
         "What comes next in the sequence: 2, 4, 6, 8, ___? ",
         "If a shirt costs $20 and is 25% off, what is the final price? ",
         "Solve the equation: 3x + 5 = 14. ",
         "If a train travels 120 miles in 2 hours, what is its speed? ",
         "What is the capital of France? ",
         "Which of the following numbers does not belong to the group? 3, 7, 11, 14, 19 ",
         "If 5 + 3 = 28 and 9 + 1 = 810, then what is 6 + 2?  ",
         "If a square has a side length of 4 units, what is its area? ",
         "Name the WONDER OF WORLD Present In India: ",
         "Who is Prime Minster Of India?  "
     ]
    
    logic_answers = ['10', '15', '3', '60', 'paris','14','48','16,','taj mahal','narendra modi']
    
    
    # Check if questions already exist in the table
    cursor.execute("SELECT * FROM carrer_questionss")
    existing_questions = cursor.fetchall()
    existing_questions = [q[1] for q in existing_questions]

    # Insert new questions if they don't exist
    for question in test_questions:
        if question not in existing_questions:
                cursor.execute("INSERT INTO carrer_questionss (question_text) VALUES (%s)", (question,))
                db.commit()
           
   
    cursor.execute("SELECT * FROM logic_questions")
    existing_questions = cursor.fetchall()
    existing_questions = [q[1] for q in existing_questions]

    # Insert new questions if they don't exist
    for question in logic_questions:
        if question not in existing_questions:
            cursor.execute("INSERT INTO logic_questions (question_text) VALUES (%s)", (question,))
            db.commit()
     
    #check answers
    cursor.execute("SELECT * FROM logic_answers")
    existing_answers = cursor.fetchall()
    existing_answers = [q[1] for q in existing_answers]
    
    #insert answers
    for answer in logic_answers:
        if answer not in existing_answers:
            cursor.execute("INSERT INTO logic_answers (answers) VALUES (%s)", (answer,))
            db.commit()
    
    
def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else None

def is_valid_password(password):
    """
    Check if the password meets the specified criteria:
    - Minimum length of 6 characters
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one special character
    """
    has_lowercase = False
    has_uppercase = False
    has_special_char = False

    for c in password:
        if c.islower():
            has_lowercase = True
        elif c.isupper():
            has_uppercase = True
        elif c in '!@#$%^&*(),.?":{}|<>':
            has_special_char = True

    return len(password) >= 6 and has_lowercase and has_uppercase and has_special_char

def signup():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Username already exists. Please choose another one.")
        else:
            # Check if the password meets the criteria
            if not is_valid_password(password):
                print('!'*15,'ERROR',"!"*15)
                print("Invalid password. Please make sure it has a minimum length of 6 characters, "
                      "at least one lowercase letter, one uppercase letter, and one special character.")
            else:
                # Insert the new user into the database
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                print("Signup successful!")
                user_menu_signup(username)
                break

def login():
    global username
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the username and password match
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    if cursor.fetchone():
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

def admin_login():
    admin_username = input("Enter admin username: ")
    admin_password = input("Enter admin password: ")

    # Check if the admin credentials are valid
    if admin_username == "admin" and admin_password == "adminpass":
        print("Admin login successful!")
        admin_menu()
    else:
        print("Invalid admin credentials.")

def admin_menu():
    while True:
      print('-'*92)
      print("                                         ADMIN MENU       ")
      print('-'*92)
      print("1. Add a new question")
      print('-'*92)
      print("2. View all questions")
      print('-'*92)
      print("3. Edit a question")
      print('-'*92)
      print("4. Delete a question")
      print('-'*92)
      print("5. Manage Logic Questions")
      print('-'*92)
      print("6. Logout")
      print('-'*92)
      admin_choice = input("Enter your choice: ")

      if admin_choice == "1":
          add_question(questions_1)
      elif admin_choice == "2":
          view_all_questions()
      elif admin_choice == "3":
          edit_question()
      elif admin_choice == "4":
          delete_question()
      elif admin_choice == "5":
          logic_questions_menu()  # Call the new function
      elif admin_choice == "6":
          break
      else:
          print("Invalid choice. Please try again.")

def logic_questions_menu():
    while True:
        print('-'*92)
        print("                       Logic Questions Menu:                      ")
        print('-'*92)
        print("1. Add a new logic question")
        print('-'*92)
        print("2. View all logic questions")
        print('-'*92)
        print("3. Delete a logic question")
        print('-'*92)
        print("4. Back to Admin Menu")
        print('-'*92)
        logic_choice = input("Enter your choice: ")

        if logic_choice == "1":
            add_logic_question()
        elif logic_choice == "2":
            view_all_logic_questions()
        elif logic_choice == "3":
            delete_logic_question()
        elif logic_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
           
def view_All_logic_answers():
    cursor.execute("select * from logic_answers")
    q=cursor.fetchall()
    for i in q:
        print(i)

def add_logic_question():
    new_question = input("Enter the new logic question: ")
    new_answer=input("Enter the answer for the question: ")
    cursor.execute("INSERT INTO logic_questions (question_text) VALUES (%s)", (new_question,))
    cursor.execute("INSERT INTO logic_answers (answers) VALUES (%s)", (new_answer,))
    db.commit()
    print("New logic question added successfully.")

def view_all_logic_questions():
    cursor.execute("SELECT * FROM logic_questions")
    q = cursor.fetchall()
    for i in q:
        print(i)


def delete_logic_question():
    view_all_logic_questions()
    question_index = int(input("Enter the index of the logic question to delete: ")) - 1
    view_All_logic_answers()
    answer_index=int(input("Enter the index of the logic questions answer to delete: ")) - 1
    cursor.execute("DELETE FROM logic_questions WHERE id = %s", (question_index + 1,))
    cursor.execute("DELETE FROM logic_answers WHERE id = %s", (answer_index + 1,))
    db.commit()
    print("Logic question and answer deleted successfully.")


def add_question(question):
    global n #n is used as a variable in carrrer recoomender
    new_question = input("Enter the new question: ")
    questions_1.append(new_question)
    cursor.execute("INSERT INTO carrer_questionss (question_text) VALUES (%s)", (new_question,))
    db.commit()
    print("New question added successfully.")
    n=n+1

def view_all_questions():
    cursor.execute("SELECT * FROM carrer_questionss")
    q = cursor.fetchall()
    for i in q:
        print(i)

def edit_question():
    view_all_questions()
    question_index = int(input("Enter the question number to be edited: "))
    new_question_text = input("Enter the updated question text: ")
    cursor.execute("UPDATE carrer_questionss SET question_text = %s WHERE id = %s", (new_question_text, question_index))
    db.commit()
    print("Question edited successfully.")

def delete_question():
    global n
    view_all_questions()
    question_index = int(input("Enter the index of the question to delete: ")) - 1
    ch=cursor.execute("select * from carrer_questionss where id=%s", (question_index + 1,))
    row=cursor.fetchone()
    ch = cursor.execute("DELETE FROM carrer_questionss WHERE id = %s", (question_index + 1,))
    n=n-1
    db.commit()
    if ch:
        cursor.execute("CREATE TABLE IF NOT EXISTS new_career_questions (id INT AUTO_INCREMENT PRIMARY KEY, question_text VARCHAR(255))")
        db.commit()
    print("Question deleted successfully.")

def retrieve_answers(user_id):
    cursor.execute("SELECT * FROM user_answers WHERE user_id = %s", (user_id,))
    return cursor.fetchall()

def save_answers(user_id, answers):
    # Delete existing answers for the user
    cursor.execute("DELETE FROM user_answers WHERE user_id = %s", (user_id,))
    db.commit()

    # Save new answers
    for answer in answers:
        cursor.execute("INSERT INTO user_answers (user_id, answer) VALUES (%s, %s)", (user_id, answer))
    db.commit()
n=7
def career_recommendation(username):
    
    global answers
    answers = []
    user_id = get_user_id(username)
    global n 

    # Check if user has already answered the questions
    ch=cursor.execute("select * from carrer_questionss" )
    questions=cursor.fetchall()
    db.commit()
   
    for question in questions:
            answer = input(question[1]).lower()
            if answer not in ['yes','no']:
                print('!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!')
                print('                PLEASE ENTER yes/no          ')
                answer = input(question).lower()
            else:
                answers.append(answer)
    
    # Analyze the answers and provide a career recommendation
    career_recommendation = "Undecided"
    if answers.count('yes') >= n+1:
        career_recommendation = "You might enjoy a career in Technology or Engineering."
    elif answers.count('yes') == n-1:
        career_recommendation = "Consider a career in Finance/Commerce"
    elif answers.count('yes') == n:
        career_recommendation = "Consider a career in Arts."
    elif answers.count('yes') <= n-2:
        career_recommendation = "Consider exploring new options."

    print("\nCareer Recommendation: {}".format(career_recommendation))
   
        # Display the recommendation using a pie chart
    labels = ['Technology/Engineering', 'Finance/Commerce', 'Creative Arts', 'Undecided']

        # Calculate the percentage distribution based on 'yes' answers
    total_yes = answers.count('yes')
    sizes = [0, 0, 0, 0]  # Initialize sizes for each category

        # Assign percentages based on the career recommendation
    if career_recommendation == "You might enjoy a career in Technology or Engineering.":
            sizes[0] = 0.6  # 60% for Technolog
            sizes[1] = 0.1  # 10% for Business
            sizes[2] = 0.1  # 10% for Creative Arts
            sizes[3] = 0.2  # 20% for Undecided
    elif career_recommendation == "Consider a career in Finance/Commerce":
            sizes[0] = 0.1  # 10% for Technology/Engineering
            sizes[1] = 0.6  # 60% for Business
            sizes[2] = 0.1  # 10% for Creative Arts
            sizes[3] = 0.2  # 20% for Undecided
    elif career_recommendation == "Consider a career in Arts.":
            sizes[0] = 0.1  # 10% for Technology/Engineering
            sizes[1] = 0.1  # 10% for Business
            sizes[2] = 0.6  # 60% for Arts
            sizes[3] = 0.2  # 20% for Undecided
    else:
            sizes[0] = 0.1  # 10% for Technology/Engineering
            sizes[1] = 0.1  # 10% for Business
            sizes[2] = 0.1  # 10% for Creative Arts
            sizes[3] = 0.7  # 70% for Undecided

# Convert percentages to actual values
    sizes = [round(size * total_yes) for size in sizes]

# Define custom colors for each category
    colors = ['#4CAF50', '#3498db', '#e74c3c', '#f39c12']

# Add a shadow to the pie chart
    explode = (0.1, 0, 0, 0)  # Explode the first slice for emphasis

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
    explode=explode, shadow=True)

    plt.title("Career Recommendation Distribution")
    plt.axis('equal')

    plt.show()
          
    if career_recommendation == "You might enjoy a career in Technology or Engineering.":
        technology_details()
    elif career_recommendation == "Consider a career in Finance/Commerce":
        business_details()
    elif career_recommendation == "Consider a career in Arts.":
         arts_details()
    else:
        career_undecided()
    # Save the answers to the database
    save_answers(user_id, answers)

def view_result(username):
    ch=True
    global questions
    global n 
    user_answers=[]
    user_id = get_user_id(username)
    user_answer = retrieve_answers(user_id)
    if len(user_answer)==0:
        print('You Have Not Taken The Career Recomendation Test!!!!!!!!')
        ch=False
    while ch:
       
        if user_answer:
            print("\nPrevious Answers:")
        for i in range(len(user_answer)):
            print(f"{i + 1}. {questions_1[i]} {user_answer[i][2]}")
        for j in user_answer:
            user_answers.append(j[2])
            
        career_recommendation = "Undecided"
        if user_answers.count('yes') >= n+1:
            career_recommendation = "You might enjoy a career in Technology or Engineering."
        elif  user_answers.count('yes') == n-1:
            career_recommendation = "Consider a career in Finance/Commerce."
        elif user_answers.count('yes') == n:
            career_recommendation = "Consider a career in Arts."
        elif user_answers.count('yes') <= n-2:
            career_recommendation = "Consider exploring new options."

        print("\nCareer Recommendation: {}".format(career_recommendation))

        # Display the recommendation using a pie chart
        labels = ['Technology/Engineering', 'Business', 'Creative Arts', 'Undecided']

        # Calculate the percentage distribution based on 'yes' answers
        total_yes = user_answers.count('yes')
        sizes = [0, 0, 0, 0]  # Initialize sizes for each category

        # Assign percentages based on the career recommendation
        if career_recommendation == "You might enjoy a career in Technology or Engineering.":
            sizes[0] = 0.6  # 60% for Technolog
            sizes[1] = 0.1  # 10% for Business
            sizes[2] = 0.1  # 10% for Creative Arts
            sizes[3] = 0.2  # 20% for Undecided
        elif career_recommendation == "Consider a career in Finance/Commerce.":
            sizes[0] = 0.1  # 10% for Technology/Engineering
            sizes[1] = 0.6  # 60% for Business
            sizes[2] = 0.1  # 10% for Creative Arts
            sizes[3] = 0.2  # 20% for Undecided
        elif career_recommendation == "Consider a career in Arts.":
            sizes[0] = 0.1  # 10% for Technology/Engineering
            sizes[1] = 0.1  # 10% for Business
            sizes[2] = 0.6  # 60% for Arts
            sizes[3] = 0.2  # 20% for Undecided
        else:
            sizes[0] = 0.1  # 10% for Technology/Engineering
            sizes[1] = 0.1  # 10% for Business
            sizes[2] = 0.1  # 10% for Creative Arts
            sizes[3] = 0.7  # 70% for Undecided

        # Convert percentages to actual values
        sizes = [round(size * total_yes) for size in sizes]

       # Define custom colors for each category
        colors = ['#4CAF50', '#3498db', '#e74c3c', '#f39c12']

        # Add a shadow to the pie chart
        explode = (0.1, 0, 0, 0)  # Explode the first slice for emphasis

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        explode=explode, shadow=True)

        plt.title("Career Recommendation Distribution")
        plt.axis('equal')

        plt.show()
       
        if career_recommendation == "You might enjoy a career in Technology or Engineering.":
            technology_details()
        elif career_recommendation == "Consider a career in Finance/Commerce.":
            business_details()
        elif career_recommendation == "Consider a career in Arts.":
             arts_details()
        else:
            career_undecided()
        break
   
   

def logic_test():
  logic_questions=[]
  logic_answers = []
  cursor.execute("select * from logic_questions")
  ch=cursor.fetchall()
  db.commit()
  for i in ch:
      logic_questions.append(i[1])
  cursor.execute("Select * from logic_answers")
  answer=cursor.fetchall()
  for i in answer:
      logic_answers.append(i[1])
      
  user_answers = []
  score = 0

  for i in range(len(logic_questions)):
        answer = input(logic_questions[i]).strip().lower()
        user_answers.append(answer)
        if answer == logic_answers[i].lower():
            score += 1
  d=score/len(logic_questions)*100

  print(f"\nLogic Test Score: {score}/{len(logic_questions)}")
  print('Your intelligince rate is:',d)
 

def user_menu_login():
    while True:
        print('-'*92)
        print("                                   USER LOGIN MENU       ")
        print('-'*92)
        print("1. View Career Recommendation")
        print('-'*92)
        print("2. Take Carrer Recoomendation Test")
        print('-'*92)
        print("3. Take Logic Test")
        print('-'*92)
        print("4. Logout")
        print('-'*92)

        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            view_result(username)
        elif user_choice == "2":
            career_recommendation(username)
        elif user_choice == "3":
            logic_test()
        elif user_choice == "4":
            break
               
        else:
            print("Invalid choice. Please try again.")
def user_menu_signup(username):
    while True:
        print('-'*92)
        print("                                      USER SIGNUP MENU       ")
        print('-'*92)
        print("1. Take Carrer Recoomendation Test")
        print('-'*92)
        print("2. Take Logic Test")
        print('-'*92)
        print("3. Signout")
        print('-'*92)
        ch=input("Enter your choice: ")
       
        if ch=="1":
            career_recommendation(username)
           
        elif ch=="2":
            logic_test()
        elif ch=="3":
            break
       
           
       
def technology_details():
    # Create a dictionary to store details
    technology_data = {
        "Jobs": ["Software Engineer", "Mechanical Engineer", "Data Scientist"],
        "Colleges/Universities": ["MIT", "Stanford", "Carnegie Mellon","IITs","BITS Pilani","Delhi University","NITs"],
        "Average Salary": "$80,000 - $120,000",  # Add your salary range here
        "Experience Level": "Entry Level/Mid-Level/Senior Level" , # Add your experience levels here
        "ENTRANCE EXAMS":["JEE MAINS","JEE ADVANCE","BITSAT","CUET","SAT","ACT"]
    }

    # Print the details
    print("\nTechnology/Engineering Details:")
    print("\nJobs:")
    for job in technology_data["Jobs"]:
        print("- {}".format(job))

    print("\nColleges/Universities:")
    for university in technology_data["Colleges/Universities"]:
        print("- {}".format(university))
       
    print("\nENTRANCE EXAM REQURIED:")
    for entrance_exams in technology_data["ENTRANCE EXAMS"]:
        print("- {}".format(entrance_exams))

    print("\nAverage Salary: {}".format(technology_data["Average Salary"]))
    print("Experience Level: {}".format(technology_data["Experience Level"]))


def business_details():
    # Create a dictionary to store details
    business_data = {
        "Jobs": ["Marketing Manager", "Financial Analyst", "Entrepreneur"],
        "Colleges/Universities": ["Harvard Business School", "Wharton School of Business", "Stanford GSB","Shri Ram College of Commerce","IIM","NMIMS","St. Xavier's College"],
        "Average Salary": "$60,000 - $100,000",  # Add your salary range here
        "Experience Level": "Entry Level/Mid-Level/Senior Level",  # Add your experience levels here
        "ENTRANCE EXAMS":["CAT","IPMAT","CUET","SAT","ACT","NSAT"]
    }

    # Print the details
    print("\nBusiness Details:")
    print("\nJobs:")
    for job in business_data["Jobs"]:
        print("- {}".format(job))

    print("\nColleges/Universities:")
    for university in business_data["Colleges/Universities"]:
        print("- {}".format(university))
       
    print("\nENTRANCE EXAM REQURIED:")
    for entrance_exams in business_data["ENTRANCE EXAMS"]:
        print("- {}".format(entrance_exams))


    print("\nAverage Salary: {}".format(business_data["Average Salary"]))
    print("Experience Level: {}".format(business_data["Experience Level"]))
   
def arts_details():
    # Create a dictionary to store details
    arts_data = {
        "Jobs": ["Graphic Designer", "Writer", "Actor/Actress"],
        "Colleges/Universities": ["School of Visual Arts", "New York Film Academy", "Julliard School","NID","NIFT"],
        "Average Salary": "$30,000 - $70,000",  # Add your salary range here
        "Experience Level": "Entry Level/Mid-Level/Senior Level" , # Add your experience levels here
        "ENTRANCE EXAMS":["CUET","SAT","ACT","NID DAT","UCEED"]
   
    }

    # Print the details
    print("\nArts Details:")
    print("\nJobs:")
    for job in arts_data["Jobs"]:
        print("- {}".format(job))

    print("\nColleges/Universities:")
    for university in arts_data["Colleges/Universities"]:
        print("- {}".format(university))
       
    print("\nENTRANCE EXAM REQURIED:")
    for entrance_exams in arts_data["ENTRANCE EXAMS"]:
        print("- {}".format(entrance_exams))

    print("\nAverage Salary: {}".format(arts_data["Average Salary"]))
    print("Experience Level: {}".format(arts_data["Experience Level"]))
   
   
def career_undecided():
    print("\nUndecided Career Options:")
    print("1. Career Counselor")
    print("2. Exploratory Internship")
    print("3. Career Development Program")
    print("4. Further Education and Skill Development")

    undecided_jobs = [
        "Administrative Assistant",
        "Customer Service Representative",
        "Sales Associate",
        "Data Entry Clerk",
    ]

    undecided_salary_ranges = [
        "$30,000 - $40,000",
        "$25,000 - $35,000",
        "$25,000 - $35,000",
        "$28,000 - $38,000",
    ]

    undecided_universities = [
        "Local Community College",
        "Online Skill Development Platforms",
        "Local Vocational Training Centers",
    ]

    print("\nUndecided Job Options:")
    for i in range(len(undecided_jobs)):
        print(f"{i + 1}. {undecided_jobs[i]} - Salary Range: {undecided_salary_ranges[i]}")

    print("\nUndecided University/Training Options:")
    for i in range(len(undecided_universities)):
        print(f"{i + 1}. {undecided_universities[i]}")

questions_1 = [
    "Do you enjoy working with numbers? (yes/no): ",
    "Are you interested in technology and computers? (yes/no): ",
    "Do you enjoy helping others? (yes/no): ",
    "Are you creative and enjoy expressing yourself? (yes/no): ",
    "Are you comfortable taking on leadership roles and making decisions for a group? (yes/no): ",
    "Do you enjoy exploring and understanding how things work in the natural world? (yes/no): ",
    "Are you good at organizing and planning events or activities? (yes/no): ",
    "Do you have a strong interest in business and entrepreneurship? (yes/no): ",
    "Are you comfortable speaking in front of a group of people? (yes/no): ",
    "Do you enjoy solving complex problems and puzzles(yes/no): ",
    "Are you comfortable working with deadlines and handling time-sensitive tasks?(yes/no): ",
    "Do you find joy in helping others understand new concepts or skills?(yes/no): ",
    "Are you interested in environmental sustainability and conservation efforts?(yes/no): ",
    "Do you enjoy analyzing and interpreting data to make informed decisions?(yes/no): ",
    "Are you interested in staying updated on the latest advancements in technology?(yes/no): ",
    "Are you interested in exploring different cultures and working in diverse environments?(yes/no): ",
    "Do you prefer a structured and organized work environment?(yes/no): "
]

logic_questions = [
     "What comes next in the sequence: 2, 4, 6, 8, ___? ",
     "If a shirt costs $20 and is 25% off, what is the final price? ",
     "Solve the equation: 3x + 5 = 14. ",
     "If a train travels 120 miles in 2 hours, what is its speed? ",
     "What is the capital of France? ",
     "Which of the following numbers does not belong to the group? 3, 7, 11, 14, 19 ",
     "If 5 + 3 = 28 and 9 + 1 = 810, then what is 6 + 2?  ",
     "If a square has a side length of 4 units, what is its area? ",
     "Name the WONDER OF WORLD Present In India: ",
     "Who is Prime Minster Of India?  "
 ]

if __name__ == "__main__":
    create_tables()
   


    while True:
        print('-'*92)
        print('                                   WELCOME TO CARRERHELPER          ')
        print('-'*92)
        print("1. Signup")
        print('-'*92)
        print("2. Login")
        print('-'*92)
        print("3. Admin Login")
        print('-'*92)
        print("4. Exit")
        print('-'*92)

        choice = input("Enter your choice: ")

        if choice == "1":
            signup()
            break
        elif choice == "2":
            if login():
                user_menu_login()
                break
        elif choice == "3":
            admin_login()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

cursor.close()
db.close()
