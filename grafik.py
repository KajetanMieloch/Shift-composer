from __future__ import annotations

 

from typing import List, Tuple


class NotEnoughEmploeesException(Exception):
    pass


# Employee class
class Employee:
    def __init__(self, name: str, surename: str, id: int,shiftsInRow :int, possibleShifts: List[List[int]], descont: bool, coordinator: bool, contract: bool,):
        self.name = name
        self.surename = surename
        self.id = id
        self.possibleShifts = possibleShifts   
        self.descont = descont
        self.coordinator = coordinator
        self.contract = contract
        self.offShifts = []
        self.shiftsInRow = shiftsInRow
        self.hadShift = False
        self.doNotAssign = False
        self.hoursInTotal = 0
        self.workedDays = []
        self.possibleShiftsCount = 0

 
days = 30

def printSchedule(schedule: List[List[Tuple[str, int, int]]]):
    for day in range(days):
        print(f"Day {day + 1}:")
        for employee_name, shift, id in schedule[day]:
            print(f"  Shift {shift}: {employee_name}")
 
def shiftsInRow(employee: Employee, day: int, modifierShiftsInRow: int):
    #Employee had shift
    employee.hadShift = True

    employee.hoursInTotal += 8

    #Number of shifts in row is increased by 1
    employee.shiftsInRow += 1
    #Number of shifts in row is reseted to -1
    if employee.shiftsInRow == modifierShiftsInRow:
        employee.shiftsInRow = -1
    
    #Add day to workedDays
    workedDays(employee, day)


 

def workedDays(employee: Employee, day: int):
    employee.workedDays.append(day)
 

 

# Get the available employees
def availableEmployees(employees: list[Employee], day: int, shift: int) -> list[Employee]:
    # Generate the employees (list comprehension)
    available_employees = [employee for employee in employees if shift in employee.possibleShifts[day] if shift not in employee.offShifts if employee.hadShift == False]
    return available_employees

 

 

#Check if there is descont employee on next shift, and if he has 2 possible shifts
def isNextShiftDescont(employees: list[Employee], day: int, shift: int) -> bool:
    # Generate the employees (list comprehension)
    available_employees = availableEmployees(employees, day, shift+1)
    descont_employee = [employee for employee in available_employees if employee.descont]
    if descont_employee:
        try:
            #If descont employee has 2 possible shifts, then he is forced to be assigned on next shift
            descont_employee[0].doNotAssign = True
        except:
            pass
        return True
    else:
        return False

 

 

#assign OffSifts for every employee
def assignEmployeeOffShifts(schedule: List[List[Tuple[str, int, int]]], day: int) -> list[Employee]:

 

    
    thisDaySchedule = [employee for employee in schedule][day]
    for n in range(len(thisDaySchedule)):
        #If employee has shift 3, then he has offShifts 1 and 2
        if thisDaySchedule[n][1] == 3:
            for employee in employees:
                if employee.id == thisDaySchedule[n][2]:
                    employee.offShifts.clear()
                    employee.offShifts.append(1)
                    employee.offShifts.append(2)
        #If employee has shift 2, then he has offShift 1
        elif thisDaySchedule[n][1] == 2:
            for employee in employees:
                if employee.id == thisDaySchedule[n][2]:
                    employee.offShifts.clear()
                    employee.offShifts.append(1)
        #If employee has shift 1, or he has no shift, then he has no offShifts
        else:
            for employee in employees:
                if employee.id == thisDaySchedule[n][2] or employee.hadShift == False:
                    employee.offShifts.clear()

 

 

def assignEmployeesByOrder(available_employees: List[Employee], schedule: List[List[Tuple[str, int, int]]], day: int, shift: int, whichInTurn: int, maxShifts: int, modifierShiftsInRow: int) -> bool:
    
    try:
        employee = available_employees.pop(whichInTurn)
        schedule[day].append((employee.name, shift, employee.id))
        shiftsInRow(employee, day, modifierShiftsInRow)
    except:
        #If there is no more employees to assign, but there are at least 2 employees on shift,
        #then go to next shift
        if len([x for x in schedule[day] if x[1] == shift]) >= 2:
            return True
        #If there is less than 2 employees on shift, then recurency is called
        else:
            reasignEmployee(schedule, day, shift, available_employees, maxShifts, "nonDescont",modifierShiftsInRow)
            #TODO Program a recurency, that will figure out what to do if there is no more employees to assign



    #Assign the descont employee (at least one per shift)
    #Sort the list of descont employees by shiftsInRow
def assignDescontEmployee(schedule: List[List[Tuple[str, int, int]]], day: int, shift: int, available_employees: List[Employee], descont_employee: List[Employee], modifierShiftsInRow: int) -> bool:
       
    descont_employee.sort(key=lambda employee: employee.shiftsInRow, reverse=True)
    schedule[day].append((descont_employee[0].name, shift, descont_employee[0].id))
    available_employees.remove(descont_employee[0])
    shiftsInRow(descont_employee[0], day, modifierShiftsInRow)

 

def isThisShiftValid(employeesOnShift :[Employee]) -> bool:
    for employee in employeesOnShift:
        if employee.descont and len(employeesOnShift) >= 2:
            return True
    
    return False

 

def reasignEmployee(schedule: List[List[Tuple[str, int, int]]], day: int, shift: int, available_employees: List[Employee], maxShifts: int, mode: str, modifierShiftsInRow: int, descont_employee = [], descontAllreadyAssigned = False):

 
    if mode == "descont":
        allEmployeesWithDescontAndPossibleShift = [employee for employee in employees if employee.descont if shift in employee.possibleShifts[day] if day-1 in employee.workedDays if not employee.hadShift if not employee.contract]

        if descontAllreadyAssigned:
            return 0

        elif not allEmployeesWithDescontAndPossibleShift:
            raise NotEnoughEmploeesException("There is no suitable descont employee")
        
        #Check if any employee in allEmployeesWithDescontAndPossibleShift is avaliable
        for nShift in range(1, maxShifts+1):
            try:
                schedule[day-1].remove((allEmployeesWithDescontAndPossibleShift[0].name, nShift, allEmployeesWithDescontAndPossibleShift[0].id))
                presentShift = []
                for nEmployee in range(0, len(schedule[day-1])):
                    if schedule[day-1][nEmployee][1] == nShift:
                        for employee in employees:
                            if employee.id == schedule[day-1][nEmployee][2]:
                                presentShift.append(employee)
                
                if not isThisShiftValid(presentShift):
                    raise NotEnoughEmploeesException("Prev shift is now incorrect due to deletion of prev employee")
                        
            except ValueError:
                pass
            
        for n in range(1, maxShifts+1):
            try:
                schedule[day-1].remove((allEmployeesWithDescontAndPossibleShift[0].name, n, allEmployeesWithDescontAndPossibleShift[0].id))
            except:
                pass
        #Assign the descont employee
        allEmployeesWithDescontAndPossibleShift[0].shiftsInRow -= 1
        descont_employee.append(allEmployeesWithDescontAndPossibleShift[0])
        available_employees.append(allEmployeesWithDescontAndPossibleShift[0])
        assignDescontEmployee(schedule, day, shift, available_employees, descont_employee, modifierShiftsInRow)

    if mode == "nonDescont":
        allEmployeesWithPossibleShift = [employee for employee in employees if shift in employee.possibleShifts[day] if day-1 in employee.workedDays if not employee.hadShift if not employee.contract]
        if not allEmployeesWithPossibleShift:
            raise NotEnoughEmploeesException("There is no suitable employee")
        #Check if any employee in allEmployeesWithDescontAndPossibleShift is avaliable
        for nShift in range(1, maxShifts+1):
            try:
                schedule[day-1].remove((allEmployeesWithPossibleShift[0].name, nShift, allEmployeesWithPossibleShift[0].id))
                presentShift = []
                for nEmployee in range(0, len(schedule[day-1])):
                    if schedule[day-1][nEmployee][1] == nShift:
                        for employee in employees:
                            if employee.id == schedule[day-1][nEmployee][2]:
                                presentShift.append(employee)
                if not isThisShiftValid(presentShift):
                    raise NotEnoughEmploeesException("Prev shift is now incorrect due to deletion of prev employee")
            except ValueError:
                pass
        for n in range(1, maxShifts+1):
            try:
                schedule[day-1].remove((allEmployeesWithPossibleShift[0].name, n, allEmployeesWithPossibleShift[0].id))
            except:
                pass
        #Assign the descont employee
        allEmployeesWithPossibleShift[0].shiftsInRow -= 1
        available_employees.append(allEmployeesWithPossibleShift[0])




# Generate the schedule
def generate_schedule(employees: list[Employee], modifierShiftsInRow: int) -> list[list[tuple[str, int, int]]]:
    try:
        schedule = [[] for _ in range(days)]

        # Generate the of days (range)
        for day in range(days):

            nonDescontPriority = False
            descontAllreadyAssigned = False

            #Set hadShift to False for all employees
            allEmployees = [employee for employee in employees]
            for employee in allEmployees:
                employee.hadShift = False
                employee.doNotAssign = False

            #define max shifts
            maxShifts = 3

            # Generate the shifts (range)
            for shift in range(1, maxShifts+1):

                available_employees = availableEmployees(employees, day, shift)

                # Get the coordinator
                coordinator = next((employee for employee in available_employees if employee.coordinator), None)

                #Get all descont employees
                descont_employee = [employee for employee in available_employees if employee.descont if employee.contract == False]
    
                # Assign the coordinator (no more than one per shift)
                if coordinator:
                    schedule[day].append((coordinator.name, shift, coordinator.id))
                    coordinator.hoursInTotal += 8

                    if len(descont_employee) < 4 and shift == 1:
                        nonDescontPriority = True
                    continue
                else:
                    if len(descont_employee) < 7 and shift == 1:
                        nonDescontPriority = True

                # Generate the contract employees (list comprehension)
                contract_employees = [employee for employee in available_employees if employee.contract]

                # Assign the contract employees
                for employee in contract_employees:
                    employee.hoursInTotal += 8
                    schedule[day].append((employee.name, shift, employee.id))
                    available_employees.remove(employee)
                    descontAllreadyAssigned = True

                #Assign the descont employee (at least one per shift)
                if descont_employee:
                    assignDescontEmployee(schedule, day, shift, available_employees, descont_employee, modifierShiftsInRow)

                #If there is no descont employee, then try delete previous shift descont employee
                elif not descont_employee:
                
                    #'schedule', 'day', 'shift', 'available_employees', and 'descont_employee'
                    reasignEmployee(schedule, day, shift, available_employees, maxShifts, "descont",modifierShiftsInRow, descont_employee, descontAllreadyAssigned)
                    
                    #raise NotEnoughEmploeesException("not enough descont employees on day " + str(day+1) + " shift " + str(shift))
    
                # Assign the rest of the employees
                available_employees.sort(key=lambda employee: employee.shiftsInRow, reverse=True)

    
                iterationOfNonDescontEmployee = 0
                iterationOfDescontEmployee = 0

                while len([x for x in schedule[day] if x[1] == shift]) < 3:

                    iterationOfNonDescontEmployee += 1
                    iterationOfDescontEmployee += 1

                    #Check if there is descont employee on next shift
                    if shift != 3:
                        if isNextShiftDescont(employees, day, shift):
                            nonDescontPriority = False


                    #If there is nonDescontPriority, then non descont employee is assigned first
                    if nonDescontPriority and iterationOfNonDescontEmployee <=3 and shift <=3:
                        for employee in available_employees:
                            if employee.descont == False and employee.doNotAssign == False:
                                schedule[day].append((employee.name, shift, employee.id))
                                available_employees.remove(employee)
                                shiftsInRow(employee, day, modifierShiftsInRow)
                                break
                    #If there is no nonDescontPriority, then descont employee is assigned first
                    #but if employee has doNotAssign set to True, then he is not assigned
                    elif iterationOfDescontEmployee <=3 and shift <=3:
                        for employee in available_employees:
                            if employee.doNotAssign == False:
                                schedule[day].append((employee.name, shift, employee.id))
                                available_employees.remove(employee)
                                shiftsInRow(employee, day, modifierShiftsInRow)
                                break

                    #Else, employee is assigned by order
                    else:
                        if employee.doNotAssign == False:                        
                            if assignEmployeesByOrder(available_employees, schedule, day, shift ,0, maxShifts, modifierShiftsInRow):
                                break   
                        else:
                            if assignEmployeesByOrder(available_employees, schedule, day, shift ,1, maxShifts, modifierShiftsInRow):
                                break

                #TODO Program a recurency, that will figure out what to do if there is no more employees to assign
                #If there is less than 2 employees on shift, then recurency is called
                if len([x for x in schedule[day] if x[1] == shift]) < 2:
                    raise NotEnoughEmploeesException("Not enough employees on shift" + str(shift) + " on day " + str(day+1))

            assignEmployeeOffShifts(schedule, day)
    
    except NotEnoughEmploeesException as e:
        return False
        #generate_schedule(employees)

 

 

    return schedule
 


#Define employees
def defineEmployees(n = 0):
    FJ = Employee("Filip", "J",1,n, [[1],[1],[1],[1],[1],[],[],[1],[1],[1],[1],[1],[],[],[1],[1],[1],[1],[1],[],[],[1],[1],[1],[1],[1],[],[],[1],[1],[1]], False,True,False)
    KM = Employee("Kacper", "M",2,n, [[2],[2],[2],[],[],[2],[2],[2],[2],[2],[],[],[2],[2],[2],[2],[2],[],[],[2],[2],[2],[2],[2],[],[],[2],[2],[2],[2],[2]], True,False,True)
    MB = Employee("Maks", "B",3,n, [[2],[2],[3],[2,3],[2,3],[1,2],[1,2],[],[],[],[],[],[1],[3],[3],[3],[2,3],[2],[2,3],[2],[2,3],[3],[],[],[],[],[2],[3],[2],[2],[2,3]], True,False,False)
    KT = Employee("Krystian", "T",4,n, [[3],[],[],[3],[3],[3],[3],[3],[],[],[3],[3],[3],[3],[3],[],[],[3],[3],[3],[3],[3],[],[],[3],[3],[3],[3],[3],[],[]], True,False,True)
    KD = Employee("Kamil", "M",5,n, [[3],[2],[3],[2],[],[],[],[],[],[],[],[],[],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[],[],[],[],[]], True,False,False)
    GW = Employee("Grzegorz", "W",6,n, [[],[],[3],[2],[2],[1],[1],[2],[],[],[2],[2],[1],[1],[2],[2],[],[],[2],[1],[1],[],[],[],[2],[2],[1],[1],[2],[2],[2]], True,False,False)
    KM2 = Employee("Kajetan", "M",7,n, [[2,3],[2],[2],[2,3],[2,3],[1,2],[1,2],[2],[2],[2],[2],[2],[1,2],[1,2],[2],[2],[2],[2],[2,3],[1,2],[1,2],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[2,3],[2,3]], False,False,False)
    PJ = Employee("Piotr", "J",8,n, [[3],[3],[3],[2,3],[2,3],[3],[3],[3],[3],[2,3],[3],[3],[3],[3],[3],[3],[2,3],[2],[2,3],[2],[],[],[],[],[],[],[],[3],[2],[2],[2,3]], True,False,False)
    KC = Employee("Kasia", "C",9,n, [[3],[3],[],[3],[],[],[],[3],[2],[3],[3],[2],[3],[3],[],[3],[3],[],[3],[],[],[],[3],[2],[3],[3],[2],[3],[3],[],[3]], True,False,False)
    DS = Employee("Damian", "S",10,n, [[2,3],[2,3],[3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[2,3],[2,3]], True,False,False)
    JG = Employee("Jakub", "G",11,n, [[],[],[],[],[],[2],[2],[3],[2,3],[2,3],[],[],[2],[3],[],[2],[2],[2],[2],[3],[],[],[],[2,3],[2,3],[2,3],[2,3],[2,3],[2],[2],[2]],True,False,True)
    MM = Employee("Mateusz", "M",12,n, [[2,3],[2],[2],[2,3],[],[1],[2],[3],[2,3],[2,3],[],[2],[],[],[],[2],[2],[2],[2],[3],[2,3],[2,3],[2,3],[2,3],[2,3],[1],[1],[],[2],[2],[2]], False,False,False)
        
    return [FJ, KM, MB, KT, KD, GW, KM2, PJ, KC, DS, JG, MM]

employees = defineEmployees()
schedule = []
 
#Generate schedules days*2 sheudles.
for day in range(-days, days+1):
    employees = defineEmployees()
    generatedSchedule = generate_schedule(employees, day)
    if generatedSchedule == False:
        pass
        print(".")
    else:
        totalHours = 0
        for employee in employees:
            totalHours +=employee.hoursInTotal
        print(totalHours)
        #Chceck if schedule is not in schedule list, if not, then add it to schedule list
        if generatedSchedule not in schedule:
            schedule.append((generatedSchedule, totalHours))


print("Generated " + str(len(schedule)) + " diffrent schedules")
print("Comparing schedules...")
schedule.sort(key=lambda x: x[1], reverse=True)
print("Best schedule:")
print(schedule[0][1])



# # Print the schedule
# for day in range(days):
#     print(f"Day {day + 1}:")
#     for employee_name, shift, id in schedule[day]:
#         print(f"  Shift {shift}: {employee_name}")

 

# totalHours = 0
# #EXPERIMETNAL FUTURE
# #Print the stats
# if day == 29:
#     print("")
#     allEmployees = [employee for employee in employees]
#     for employee in allEmployees:
#         print(f"{employee.name} worked {employee.hoursInTotal} hours in total")
#         totalHours +=employee.hoursInTotal
# print(totalHours)
