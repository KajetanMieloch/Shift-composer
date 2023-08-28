from typing import List, Tuple
from generator import generate_schedule, days
from employees import Employee, defineEmployees
from statistics import stdev, mean

schedule = []

def printSchedule(schedule: List[List[Tuple[str, int, int]]]):

    for day in range(days):

        print(f"Day {day + 1}:")

        for employee_name, shift, id in schedule[day]:

            print(f"  Shift {shift}: {employee_name}")



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

        fairnessArr = []

        for employee in employees:

            fairnessArr.append(ratioOfPossibleShiftsToTotalHours(employee))

            totalHours += employee.hoursInTotal

        fairnessRatio = calculateFairnessRatios(fairnessArr)

        #Chceck if schedule is not in schedule list, if not, then add it to schedule list

        if generatedSchedule not in schedule:

            schedule.append((generatedSchedule, totalHours, fairnessRatio))





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

option = int(input("Choose option: "))



if option == 1:

    schedule.sort(key=lambda x: x[1], reverse=True)

    printSchedule(schedule[0][0])

    print("Total hours: " + str(schedule[0][1]))

    print("Fair ratio: " + str(schedule[0][2]))

elif option == 2:

    schedule.sort(key=lambda x: x[1])

    printSchedule(schedule[0][0])

    print("Total hours: " + str(schedule[0][1]))

    print("Fair ratio: " + str(schedule[0][2]))

elif option == 3:

    schedule.sort(key=lambda x: x[2])

    printSchedule(schedule[0][0])

    print("Fair ratio: " + str(schedule[0][2]))

    print("Total hours: " + str(schedule[0][1]))

elif option == 4:

    schedule.sort(key=lambda x: x[2], reverse=True)

    printSchedule(schedule[0][0])

    print("Fair ratio: " + str(schedule[0][2]))

    print("Total hours: " + str(schedule[0][1]))

elif option == 5:

    schedule.sort(key=lambda x: x[1], reverse=True)

    schedule.sort(key=lambda x: x[2])

    printSchedule(schedule[0][0])

    print("Total hours: " + str(schedule[0][1]))

    print("Fair ratio: " + str(schedule[0][2]))



print("Would you like to save this schedule in PDF, TXT or CSV file?")

print("COMING SOON")
