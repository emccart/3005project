import psycopg2
from getpass import getpass
import datetime

dbname = input("Database name?\n")
user = input("user?\n")
password = getpass("password?\n")
host = getpass("host address?\n")
port = input("port?\n")

connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

cur = connection.cursor()

def fakePassHash(str):
    return str+"hashed"

def register(cur):
    email = input("Email? ")
    password = getpass("Password? ")
    name = input("Name? ")
    trainer = input("Are you a trainer? [y/n] ")[0] == 'y'
    t = "FALSE"
    if(trainer): t = "TRUE"
    cur.execute("INSERT INTO Users (email, passw, name, is_trainer) VALUES ('" + email + "', '" + fakePassHash(password) + "', '" + name + "', '" + t +"')")
    print("Registered")

def login(cur):
    email = input("Email? ")
    password = getpass("Password? ")
    cur.execute("SELECT * FROM Users WHERE email = '" + email + "' AND passw = '" + fakePassHash(password) + "'")
    results = cur.fetchall()
    if(len(results) != 1):
        return

    user = results[0] # tuple of values in order
    trainer = user[4]
    if(email == "admin"):
        adminMenu(cur)
    elif(trainer):
        trainerMenu(cur, user)
    else:
        memberMenu(cur, user)

def getDashboardMetrics(cur, userid):
    metrics = ['0','0','0'] # classes attended, goals set, goals met
    cur.execute("SELECT COUNT(att_id) FROM Attendance WHERE member_id = " + userid)
    metrics[0] = str(cur.fetchone()[0])
    cur.execute("SELECT COUNT(goal_id) FROM Goals WHERE member_id = " + userid)
    metrics[1] = str(cur.fetchone()[0])
    cur.execute("SELECT COUNT(goal_id) FROM Goals WHERE member_id = " + userid + " AND completed = TRUE")
    metrics[2] = str(cur.fetchone()[0])
    return metrics

def getNextAppointment(cur, userid):
    str = "None"
    cur.execute("SELECT * FROM Classes NATURAL JOIN (SELECT class_id FROM Attendance WHERE member_id = " + userid + ") NATURAL JOIN Rooms ORDER BY start_date DESC LIMIT 1")
    nextclasslist = cur.fetchall()
    if(len(nextclasslist) != 0):
        nextclass = nextclasslist[0]
        str = nextclass[4] + " in the " + nextclass[8] + " at " + nextclass[5].strftime('%I:%M') + " on " + nextclass[7].strftime('%b %d')
    return str

def displayMemberDashboard(cur, userid):
    print()
    dashboardMetrics = getDashboardMetrics(cur, userid)
    nextAppointment = getNextAppointment(cur, userid)
    print("Classes/Training attended: " + dashboardMetrics[0] + "\tGoals set: " + dashboardMetrics[1] + "\tGoals met: " + dashboardMetrics[2])
    print("Next appointment: " + nextAppointment)

def showProfile(user):
    print(user[3] +"\n"+ user[1])

def changeName(cur, user):
    newname = input("New name? ")
    cur.execute("UPDATE Users SET name = '" + newname + "' WHERE user_id = " + str(user[0]))
    user = (user[0], user[1], user[2], newname, user[4])
    print("name changed to " + newname)
    return user

def changeEmail(cur, user):
    newemail = input("New email? ")

    cur.execute("SELECT COUNT(user_id) FROM Users WHERE email = '" + newemail + "'")
    results = cur.fetchone()
    #print(results)
    if(results[0] == 0):
        cur.execute("UPDATE Users SET email = '" + newemail + "' WHERE user_id = " + str(user[0]))
        user = (user[0], newemail, user[2], user[3], user[4])
        print("email changed to "+ newemail)
    else:
        print("A user with that email already exists")
    return user

def changePassword(cur, userid):
    newpass = fakePassHash(getpass("New pass? "))
    cur.execute("UPDATE Users SET passw = '" + newpass + "' WHERE user_id = " + userid)
    print("password changed")

def personalInfoMenu(cur, user):
    x = '0'
    while(x != '4'):
        x = input("1. Change Name\n2. Change Email\n3. Change Password\n4. Return to Menu\n")
        if(x == '1'):
            user = changeName(cur, user)
        elif(x == '2'):
            user = changeEmail(cur, user)
        elif(x == '3'):
            changePassword(cur, str(user[0]))
    return user

def newGoal(cur, userid):
    desc = input("What is your goal?\n")
    cur.execute("INSERT INTO Goals (member_id, descript) VALUES (" + userid + ", '" + desc + "')")

def completeGoal(cur, goals):
    index = int(input("Which goal? "))
    id = str(goals[index][0])
    cur.execute("UPDATE Goals SET completed = TRUE WHERE goal_id = " + id)
    goals[index] = (goals[index][0], goals[index][1], goals[index][2], True)

def removeGoal(cur, goals):
    index = int(input("Which goal? "))
    id = str(goals[index][0])
    cur.execute("DELETE FROM Goals WHERE goal_id = " + id)
    goals.pop(index)

def goalMenu(cur, userid):
    cur.execute("SELECT * FROM Goals WHERE member_id = " + userid)
    goals = cur.fetchall()

    x = '0'
    while(x != '4'):
        print()
        for i in range(len(goals)):
            print(str(i) + ". " + goals[i][2], end=':')
            if(goals[i][3]):
                print(" Complete")
            else:
                print(" Incomplete")
        x = input("\n1. Set New Goal\n2. Complete Goal\n3. Remove Goal\n4. Return to Menu\n")
        if(x == '1'):
            newGoal(cur, userid)
            return
        elif(x == '2'):
            completeGoal(cur, goals)
        elif(x == '3'):
            removeGoal(cur, goals)
            return

def profileMenu(cur, user):
    x = '0'
    while(x != '3'):
        x = input("1. Edit Personal Info\t2. Edit Goals\t3. Return To Menu\n")
        if(x == '1'):
            user = personalInfoMenu(cur, user)
        elif(x == '2'):
            goalMenu(cur, str(user[0]))
    return user

def scheduleAppointment(cur, userid):
    print()
    cur.execute("SELECT * FROM CLASSES WHERE start_date >= CURRENT_DATE")
    classes = cur.fetchall()
    for i in range(len(classes)):
        print(str(i+1) + ". " + classes[i][4])
    x = input("Which class would you like to join? Enter 0 to abort ")
    if(x == '0'): return
    cur.execute("INSERT INTO Attendance (class_id, member_id) VALUES (" + str(classes[int(x) - 1][0]) + ", " + userid + ")")
    print("Class Joined")


def memberMenu(cur, user):
    userid = str(user[0])
    x = '0'
    while(x != '3'):
        displayMemberDashboard(cur, userid)
        x = input("Select an option:\n1. View/Customize Profile\n2. Book Class/Training\n3. Log Out\n")
        if(x == '1'):
            showProfile(user)
            user = profileMenu(cur, user)
        elif(x == '2'):
            scheduleAppointment(cur, userid)

def addClass(cur, userid):
    cur.execute("SELECT * FROM Rooms")
    rooms = cur.fetchall()
    for i in range(len(rooms)):
        print(str(i+1) + ". " + rooms[i][1])
    x = input("Which Room? Enter 0 to abort")
    if(x == '0'): return
    capacity = input("How many can attend? ")
    name = input("What is the class called? ")
    start = input("When does it start? ")
    duration = input("How long does it run? ")
    date = input("What date? ")
    cur.execute("INSERT INTO Classes (teacher_id, room_id, capacity, class_name, start_time, duration, start_date) VALUES (" + userid + ", " + x + ", " + capacity + ", '" + name + "', '" + start + "', '" + duration + "', '" + date + "')")
    print("Class Added")


def updateSchedule(cur, userid):
    cur.execute("SELECT * FROM Classes WHERE teacher_id = " + userid )
    classes = cur.fetchall()
    for i in range(len(classes)):
        print(str(i+1) + ". ", end='')
        print(classes[i])
    x = 0
    x = input("Cancel which class? Enter 0 to quit ")
    if(x != '0'):
        classid = str(classes[int(x) - 1][0])
        cur.execute("DELETE FROM Classes WHERE class_id = " + classid)
        cur.execute("DELETE FROM Attendance WHERE class_id = " + classid)
            

def scheduleMenu(cur, userid):
    x = 0
    while(x != '3'):
        x = input("\n1. New Class\n2. Cancel Class\n3. Quit\n")
        if(x == '1'):
            addClass(cur, userid)
        elif(x == '2'):
            updateSchedule(cur, userid)

def profileSearch(cur):
    searcharg = input("Who are you looking for?  ")
    cur.execute("SELECT (user_id, email, name) FROM Users WHERE is_trainer = FALSE AND email <> 'admin' AND name LIKE '%" + searcharg + "%'")
    results = cur.fetchall()
    for i in range(1, len(results)+1):
        result = results[i-1][0].strip('(').strip(')').split(',')
        print(str(i) + ". " + result[2] + ", " + result[1])
    
    index = int(input("Which of these users? Enter 0 to quit  "))
    if(index != 0):
        result = results[index-1][0].strip('(').strip(')').split(',')
        user = (result[0], result[1], "", result[2])
        showProfile(user)

def trainerMenu(cur, user):
    userid = str(user[0])
    x = '0'
    while(x != '3'):
        x = input("1. Update Schedule\n2. Search Members\n3. Log Out\n")
        if(x == '1'):
            scheduleMenu(cur, userid)
        elif(x == '2'):
            profileSearch(cur)

def roomManager(cur):
    cur.execute("SELECT * FROM Rooms")
    rooms = cur.fetchall()
    for r in rooms:
        print(r)
    
    index = input("Which room?  ")
    cur.execute("SELECT * FROM Classes WHERE room_id = " + index)
    classesinroom = cur.fetchall()
    print(classesinroom)

def equipmentManager(cur):
    cur.execute("SELECT * FROM Equipment")
    equipment = cur.fetchall()
    for e in equipment:
        print(e)
    
    equip_id = 0
    while(equip_id != '0'):
        equip_id = input("Update which equipment? Enter 0 to quit  ")[0]
        if(equip_id != '0'):
            cur.execute("UPDATE Equipment SET last_maint = CURRENT_DATE WHERE equip_id = " + equip_id)
            print("Maintenance Confirmed")

def classManager(cur):
    cur.execute("SELECT * FROM Users WHERE is_trainer = TRUE")
    trainers = cur.fetchall()
    for t in trainers:
        print(t)
    
    trainerid = input("Which trainer? Enter 0 to quit  ")[0]
    if(trainerid == '0'):
        return
    scheduleMenu(cur, trainerid)

def paymentManager(cur):
    cur.execute("SELECT * FROM Payments")
    payments = cur.fetchall()
    for p in payments:
        print(p)

def adminMenu(cur):
    x = '0'
    while(x != '5'):
        x = input("1. Room Management\n2. Equipment Maintenance\n3. Class Scheduling\n4. Payments\n5. Log Out\n")
        if(x == '1'):
            roomManager(cur)
        elif(x == '2'):
            equipmentManager(cur)
        elif(x == '3'):
            classManager(cur)
        elif(x == '4'):
            paymentManager(cur)

x = '0'
while(x != '3'):
    x = input("1. Register\t2. Login\t3. Exit\n")
    if(x == '1'):
        register(cur)
    elif(x == '2'):
        login(cur)
    connection.commit()

connection.close()