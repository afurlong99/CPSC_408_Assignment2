import sqlite3
import pandas as pd
from pandas import DataFrame
# Creating Cursor and converting data to SQL
conn = sqlite3.connect('./StudentDB.db')
c = conn.cursor()
data = pd.read_csv('/Users/alekseifurlong/Documents/CPSC_Courses/CPSC_408/students.csv')
data.to_sql('Student', conn, if_exists='append', index=False)
#c.execute('DROP TABLE Student;')
#c.execute('CREATE TABLE Student( StudentId INTEGER PRIMARY KEY AUTOINCREMENT, FirstName TEXT,LastName TEXT,GPA REAL, Major TEXT,FacultyAdvisor TEXT,Address TEXT,City TEXT, State TEXT,ZipCode TEXT,MobilePhoneNumber TEXT,isDeleted INTEGER);')
def checkStudentData():
    c.execute('SELECT * FROM Student')
    output = c.fetchall()
    if output == []:
        with open("students.csv") as File:
            title = 0
            for line in File:
                #Line to seperate Column line with first row
                if title == 0:
                    title += 1
                    continue
                else:
                    filter = line.split(",")
                    filter.append(title)
                    c.execute('INSERT INTO Student(FirstName,LastName,Address,City,State,ZipCode,MobilePhoneNumber,Major,GPA,StudentId) VALUES(?,?,?,?,?,?,?,?,?,?)',filter)

                    conn.commit()
                    filter.clear()
                    title += 1
    else:
        pass
# UserInterface that provides a menu
def UserInterface():
    while True:
        print("Menu: ")
        print("1. Display Students ")
        print("2. Add Student ")
        print("3. Update Student ")
        print("4. Delete Student ")
        print("5. Search Students ")
        print("6. Exit" )
        menu = input(" Choose Option: ")
        if menu == "1":
            Display()
        elif menu == "2":
            Add()
        elif menu == "3":
            Update()
        elif menu == "4":
            Delete()
        elif menu == "5":
            Search()
        elif menu == "6":
            print("Exit Program")
            c.execute('DELETE FROM Student')
            conn.commit()
            break
        else:
            print("Incorrect Input")
            continue
#  Function that shows student table
def Display():
    c.execute('SELECT * FROM Student')
    displayData = c.fetchall()
    df = DataFrame(displayData, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
    print(df)
# Function to add student
def Add():
    inputFN = input("First Name: ")
    inputLN = input("Last Name: ")
    while True:
        try:
            inputGPA = float(input("Student GPA (Decimal): "))
            break
        # GPA form checker
        except ValueError:
            print("Incorrect Form (Ex.#.##) ")
    inputMaj = input("Major: ")
    inputFA = input("Faculty Advisor: ")
    inputAd = input("Address: ")
    inputCit = input("City: ")
    inputSt = input("State: ")
    while True:
        try:
            inputZip = int(input("ZipCode: "))
            break
        # Zipcode form checker
        except ValueError:
            print("Incorrect Form. Must be 5 number Zipcode: ")
    while True:
        try:
            inputPN = input("Mobile Phone Number: ")
            break
        # Mobile Phone form checker
        except ValueError:
            print("Incorrect Form. Must only with digits: ")
    c.execute('INSERT INTO Student(FirstName,LastName,GPA,Major,FacultyAdvisor,Address,City,State,ZipCode,MobilePhoneNumber,isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (inputFN,inputLN,inputGPA,inputMaj,inputFA,inputAd,inputCit,inputSt,inputZip,inputPN,0))
    conn.commit()
    print("Student Added.")
def Update():
    inputSiD = input("ID: ")
    c.execute('SELECT * FROM Student WHERE StudentID = ?', (inputSiD,))
    output = c.fetchall()
    # If output comes out with nothing
    if output == []:
        print("Incorrect Input.")
        Update()
    else:
        print("Categories below are available:")
        print("1. Major")
        print("2. Advisor")
        print("3. Mobile Number")
        choice = input("Choose Option:")
        if choice == "1":
            # Change Major based on student ID
            inputMaj = input("Major: ")
            c.execute('UPDATE Student SET Major = ? WHERE studentID = ?', (inputMaj,inputSiD))
            conn.commit()
            print("Major Updated")
        elif choice == "2":
            # Change Faculty Advisor based on student ID
            nAdvisor = input("Advisor: ")
            c.execute('UPDATE Student SET FacultyAdvisor = ? WHERE studentID = ?', (nAdvisor,inputSiD))
            conn.commit()
            print("Advisor Updated")
        elif choice == "3":
            while True:
                try:
                    inputPN = input("Mobile Number: ")
                    break
                except ValueError:
                    # Mobile Phone form checker
                    print("Incorrect Form. Must only with digits: ")
            # Change Mobile Phone based on student ID
            c.execute('UPDATE Student SET MobilePhoneNumber = ? WHERE studentID = ?', (inputPN,inputSiD))
            conn.commit()
            print("Mobile Number Updated")
        else:
            print("Incorrect Input")
            Update()
def Delete():
    inputSiD = input("ID: ")
    c.execute('SELECT * FROM Student WHERE StudentID = ?', (inputSiD,))
    output = c.fetchall()
    # If output comes out with nothing
    if output == []:
        print("Incorrect Input.")
        Delete()
    else:
        c.execute('UPDATE Student SET isDeleted = ? WHERE studentID = ?', (1,inputSiD))
    conn.commit()
    print("Student Deleted")
def Search():
    print("Categories below are available: ")
    print("1. Major")
    print("2. GPA")
    print("3. City")
    print("4. State")
    print("5. Faculty Advisor")
    while True:
        choice = input("Choose Option: ")
        if choice == "1":
            # Select Major
            c.execute('SELECT DISTINCT Major FROM Student')
            output = c.fetchall()
            df = DataFrame(output, columns=['Majors'])
            print(df)
            filterInput = input("Major: ")
            c.execute('SELECT * FROM Student WHERE Major = ?', (filterInput,))
            output = c.fetchall()
            if output == []:
                print("Incorrect Input.")
                Search()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "2":
            # Select GPA
            filterInput = input("GPA: ")
            c.execute('SELECT * FROM Student WHERE GPA = ?', (filterInput,))
            output = c.fetchall()
            if output == []:
                print("Incorrect Input.")
                Search()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "3":
            # Select City
            c.execute('SELECT DISTINCT City FROM Student')
            output = c.fetchall()
            df = DataFrame(output, columns=['Cities'])
            print(df)
            filterInput = input("City: ")
            c.execute('SELECT * FROM Student WHERE City = ?', (filterInput,))
            output = c.fetchall()
            if output == []:
                print("Incorrect Input.")
                Search()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "4":
            # Select State
            c.execute('SELECT DISTINCT State FROM Student')
            output = c.fetchall()
            df = DataFrame(output, columns=['States'])
            print(df)
            filterInput = input("State: ")
            c.execute('SELECT * FROM Student WHERE State = ?', (filterInput,))
            output = c.fetchall()
            if output == []:
                print("Incorrect Input.")
                Search()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "5":
            # Select Faculty Advisor
            c.execute('SELECT DISTINCT FacultyAdvisor FROM Student')
            output = c.fetchall()
            df = DataFrame(output, columns=['Advisors'])
            print(df)
            filterInput = input("Faculty Advisor: ")
            c.execute('SELECT * FROM Student WHERE FacultyAdvisor = ?', (filterInput,))
            output = c.fetchall()
            if output == []:
                print("Incorrect Input.")
                Search()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        else:
            print("Incorrect Input.")
            Search()
            break
if __name__ == '__main__':
    checkStudentData()
    UserInterface()