from typing import List, Tuple
from generator import generate_schedule, days, NotEnoughEmploeesException, allErrors
from employees import Employee, defineEmployees
from statistics import stdev, mean
from PDFgenerator import generatePDF

schedule = []

def getAllEmployees(employees: List[Employee]) -> List[Employee]:
    listOfAllEmployees = []
    for employee in employees:
        listOfAllEmployees.append(employee.name + " " + employee.surename + " " + str(employee.id))
    return listOfAllEmployees

listOfAllEmployees = getAllEmployees(defineEmployees())

def printSchedule(schedule: List[List[Tuple[str, int, int]]]):

    for day in range(days):

        print(f"Day {day + 1}:")

        for employee_name, shift, id, employee_surename in schedule[day]:

            print(f"  Shift {shift}: {employee_name}")


def saveScheduleToTXT(schedule: List[List[Tuple[str, int, int]]], filename: str, stats: str = None):
    with open(filename, 'w') as f:
        for day in range(len(schedule)):
            f.write(f"Day {day + 1}:\n")
            for employee_name, shift, id, employee_surename in schedule[day]:
                f.write(f"  Shift {shift}: {employee_name} {employee_surename} {id}\n")
        
        if stats:
            f.write(stats)

def saveScheduleToTXTToBeProcessed(schedule: List[List[Tuple[str, int, int]]], filename: str, stats: str = None):
    with open(filename, 'w') as f:
        for day in range(len(schedule)):
            f.write(f"#@$^% {day + 1}\n")
            employees = set()
            for employee_name, shift, id, employee_surename in schedule[day]:
                f.write(f"%^$@# {employee_name} {employee_surename} {id} {shift}\n")
                employees.add(employee_name)
            
            for employee in listOfAllEmployees:
                if employee.split()[0] not in employees:
                    f.write(f"%^$@# {employee.split()[0]} {employee.split()[1]} {employee.split()[2]} 0\n")
        
        if stats:
            f.write(stats)
            
def ratioOfPossibleShiftsToTotalHours(employee: Employee) -> float:

    everyPossibleShift = sum([len(shift) for shift in employee.possibleShifts])

    if employee.hoursInTotal != 0:

        return everyPossibleShift/employee.hoursInTotal



def calculateFairnessRatios(array: List[float]) -> float:

    row_mean = mean(array)

    row_stdev = stdev(array)

    return row_stdev / row_mean


#Generate schedules days*2 sheudles.

for day in range(-days, days+1):

    employees = defineEmployees()

    generatedSchedule = generate_schedule(employees, day)

    if generatedSchedule == False:

        pass

    else:

        totalHours = 0

        employeesHours = []

        fairnessArr = []

        for employee in employees:

            fairnessArr.append(ratioOfPossibleShiftsToTotalHours(employee))

            totalHours += employee.hoursInTotal
            employeesHours.append(str(employee.id) + " " + str(employee.hoursInTotal))

        fairnessRatio = calculateFairnessRatios(fairnessArr)

        #Chceck if schedule is not in schedule list, if not, then add it to schedule list

        if generatedSchedule not in schedule:

            schedule.append((generatedSchedule, totalHours, fairnessRatio, employeesHours))





print("Generated " + str(len(schedule)) + " diffrent schedules")

print("Comparing schedules...")

print("Wich schedule do you want to see?")

print("1. Schedule with the most hours")

print("2. Schedule with the least hours")

print("3. Schedule with the most fair ratio")

print("4. Schedule with the least fair ratio")

print("5. Schedule with the most hours and the most fair ratio")

print("Fair ratio is calculated by dividing the number of disposition by the number of hours worked")

print("In fair ratio, the lower the better")

isThereShedule = True
option = int(input("Choose option: "))

try:
    if option == 1:

        schedule.sort(key=lambda x: x[1], reverse=True)

    elif option == 2:

        schedule.sort(key=lambda x: x[1])

    elif option == 3:

        schedule.sort(key=lambda x: x[2])

    elif option == 4:

        schedule.sort(key=lambda x: x[2], reverse=True)

    elif option == 5:

        schedule.sort(key=lambda x: x[1], reverse=True)

        schedule.sort(key=lambda x: x[2])

    
    else:
        print("\nWrong option")
except IndexError:
    print("\n++++++++++++++++++++++++++++++")
    print("+There is no schedule to show+")
    print("++++++++++++++++++++++++++++++\n")
    farthestDay = sorted(allErrors.getErrors(),key=lambda x: x[0], reverse=True)[0][0] +1
    farthestDayShift = sorted(allErrors.getErrors(),key=lambda x: x[0], reverse=True)[0][1]
    print("Try to modify day " + str(farthestDay) + " shift " + str(farthestDayShift) + " and try again")
    print("\n")
    isThereShedule = False

if isThereShedule:
    print("\nGenerated TXT and PDF file!")
    
    saveScheduleToTXT(schedule[0][0], "schedule.txt", f"Total hours: {schedule[0][1]}\nFair ratio: {schedule[0][2]}\nEmployees hours: {schedule[0][3]}")
    saveScheduleToTXTToBeProcessed(schedule[0][0], "output.txt", f"Total hours: {schedule[0][1]}\nFair ratio: {schedule[0][2]}\nEmployees hours: {schedule[0][3]}")
    generatePDF()
    
else:
    print("No schedule to save\n")
