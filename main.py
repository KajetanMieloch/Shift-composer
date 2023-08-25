from typing import List, Tuple


#Number of days in schedule
days = 3



# Employee class
class Employee:
    def __init__(self, name: str, surename: str, possibleShifts: List[List[int]], descont: bool, coordinator: bool, contract: bool):
        self.name = name
        self.surename = surename
        self.possibleShifts = possibleShifts   
        self.descont = descont
        self.coordinator = coordinator
        self.contract = contract
        self.offShifts = []
        self.shiftsInRow = 0
        self.hadShift = False
        self.doNotAssign = False


def shiftsInRow(employee: Employee):
    #Employee had shift
    employee.hadShift = True
    
    #Number of shifts in row is increased by 1
    employee.shiftsInRow += 1
    #Number of shifts in row is reseted to -1
    if employee.shiftsInRow == 5:
        employee.shiftsInRow = -1

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

# Generate the schedule
def generate_schedule(employees: list[Employee]) -> list[list[tuple[str, int]]]:
    schedule = [[] for _ in range(days)]
    
    # Generate the of days (range)
    for day in range(days):
        
               
        nonDescontPriority = False
        
        #Set hadShift to False for all employees
        allEmployees = [employee for employee in employees]
        for employee in allEmployees:
            employee.hadShift = False
            employee.doNotAssign = False

        # Generate the shifts (range)
        for shift in [1, 2, 3]:
            
            # Get the available employees
            available_employees = availableEmployees(employees, day, shift)

            # Get the coordinator
            coordinator = next((employee for employee in available_employees if employee.coordinator), None)
            
            #Get all descont employees
            descont_employee = [employee for employee in available_employees if employee.descont]
            
            # Assign the coordinator (no more than one per shift)  
            if coordinator:
                schedule[day].append((coordinator.name, shift))
                
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
                schedule[day].append((employee.name, shift))
                available_employees.remove(employee)
            
            #Assign the descont employee (at least one per shift)
            #Sort the list of descont employees by shiftsInRow
            descont_employee.sort(key=lambda employee: employee.shiftsInRow, reverse=True)
            if descont_employee:
                schedule[day].append((descont_employee[0].name, shift))
                available_employees.remove(descont_employee[0])
                descontAlreadyAssigned = True
                shiftsInRow(descont_employee[0])
                
                
            elif not descont_employee:                     
                raise Exception("not enough descont employees on day " + str(day+1) + " shift " + str(shift))
            
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
                if nonDescontPriority and iterationOfNonDescontEmployee != 3 and shift != 3:
                    for employee in available_employees:
                        if employee.descont == False and employee.doNotAssign == False:
                            schedule[day].append((employee.name, shift))
                            available_employees.remove(employee)
                            shiftsInRow(employee)
                            break
                #If there is no nonDescontPriority, then descont employee is assigned first
                #but if employee has doNotAssign set to True, then he is not assigned
                elif iterationOfDescontEmployee != 3 and shift != 3:
                    for employee in available_employees:
                        if employee.doNotAssign == False:
                            schedule[day].append((employee.name, shift))
                            available_employees.remove(employee)
                            shiftsInRow(employee)
                            break
                
                #Else, employee is assigned by order
                else:
                    if employee.doNotAssign == False:                        
                        try:
                            employee = available_employees.pop(0)
                            schedule[day].append((employee.name, shift))
                            shiftsInRow(employee)
                        except:
                            #If there is no more employees to assign, but there are at least 2 employees on shift,
                            #then go to next shift
                            if len([x for x in schedule[day] if x[1] == shift]) >= 2:
                                break
                            #If there is less than 2 employees on shift, then recurency is called
                            else:
                                #TODO Program a recurency, that will figure out what to do if there is no more employees to assign
                                raise Exception("Not enough employees on shift")
                    else:
                        try:
                            employee = available_employees.pop(1)
                            schedule[day].append((employee.name, shift))
                            shiftsInRow(employee)
                        except:
                            #If there is no more employees to assign, but there are at least 2 employees on shift,
                            #then go to next shift
                            if len([x for x in schedule[day] if x[1] == shift]) >= 2:
                                break
                            #If there is less than 2 employees on shift, then recurency is called
                            else:
                                #TODO Program a recurency, that will figure out what to do if there is no more employees to assign
                                raise Exception("Not enough employees on shift")
                            
            #TODO Program a recurency, that will figure out what to do if there is no more employees to assign
            #If there is less than 2 employees on shift, then recurency is called
            if len([x for x in schedule[day] if x[1] == shift]) < 2:
                raise Exception("Not enough employees on shift")

        prevDaySchedule = [employee for employee in schedule][day]
        for n in range(len(prevDaySchedule)):
            if prevDaySchedule[n][1] == 3:
                for employee in employees:
                    if employee.name == prevDaySchedule[n][0]:
                        employee.offShifts.clear()
                        employee.offShifts.append(1)
                        employee.offShifts.append(2)
            elif prevDaySchedule[n][1] == 2:
                for employee in employees:
                    if employee.name == prevDaySchedule[n][0]:
                        employee.offShifts.clear()
                        employee.offShifts.append(1)
            else:
                for employee in employees:
                    if employee.name == prevDaySchedule[n][0]:
                        employee.offShifts.clear()


    return schedule
 

PJ = Employee("Maryja", "J", [[2],[2],[2]], True,False,False)
KM2 = Employee("Brutusia", "M", [[2],[2],[]], False,False,False)
KM3 = Employee("Gosia", "M", [[3],[2],[2,3]], True,False,False)
KM1 = Employee("UmowaPraca - Krystian", "M", [[],[],[]], False,False,True)
DS = Employee("Kajetan", "S", [[3],[3],[3]], False,False,False)
MB = Employee("Maks", "B", [[2],[],[2,3]], False,False,False)
KC = Employee("Kasia", "C", [[],[3],[]], True,False,False)
BM = Employee("Basia", "M", [[3],[],[3]], False,False,False)
KT = Employee("UmowaPraca - Kacper", "T", [[],[],[]], False,False,True)
FJ = Employee("Koordynator", "J", [[1],[1],[1]], False,True,False)



employees = [PJ, KM1, DS, MB, KT, FJ, KC, BM, KM2, KM3]

# Generate the schedule
schedule = generate_schedule(employees)

# Print the schedule
for day in range(days):
    print(f"Day {day + 1}:")
    for employee_name, shift in schedule[day]:
        print(f"  Shift {shift}: {employee_name}")
