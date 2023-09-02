from __future__ import annotations
from typing import List, Tuple
from employees import Employee

days = 30
global allErrors

class NotEnoughEmploeesException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.allErrors = []

    def addError(self, day, shift):
        self.allErrors.append((day, shift))
        
    def getErrors(self):
        return self.allErrors

allErrors = NotEnoughEmploeesException("")


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
def assignEmployeeOffShifts(schedule: List[List[Tuple[str, int, int]]], day: int, employees: List[Employee]) -> list[Employee]:
    
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


def assignEmployeesByOrder(available_employees: List[Employee], schedule: List[List[Tuple[str, int, int]]], day: int, shift: int, whichInTurn: int, maxShifts: int, modifierShiftsInRow: int, employees: List[Employee]) -> bool:
    
    try:
        employee = available_employees.pop(whichInTurn)
        schedule[day].append((employee.name, shift, employee.id, employee.surename))
        shiftsInRow(employee, day, modifierShiftsInRow)
    except:
        #If there is no more employees to assign, but there are at least 2 employees on shift,
        #then go to next shift
        if len([x for x in schedule[day] if x[1] == shift]) >= 2:
            return True
        #If there is less than 2 employees on shift, then recurency is called
        else:
            reasignEmployee(schedule, day, shift, available_employees, maxShifts, "nonDescont",modifierShiftsInRow, employees)
            #TODO Program a recurency, that will figure out what to do if there is no more employees to assign

    #Assign the descont employee (at least one per shift)
    #Sort the list of descont employees by shiftsInRow
def assignDescontEmployee(schedule: List[List[Tuple[str, int, int]]], day: int, shift: int, available_employees: List[Employee], descont_employee: List[Employee], modifierShiftsInRow: int) -> bool:
       
    descont_employee.sort(key=lambda employee: employee.shiftsInRow, reverse=True)
    schedule[day].append((descont_employee[0].name, shift, descont_employee[0].id, descont_employee[0].surename))
    available_employees.remove(descont_employee[0])
    shiftsInRow(descont_employee[0], day, modifierShiftsInRow)


def isThisShiftValid(employeesOnShift :[Employee]) -> bool:
    for employee in employeesOnShift:
        if employee.descont and len(employeesOnShift) >= 2:
            return True
    
    return False


def reasignEmployee(schedule: List[List[Tuple[str, int, int]]], day: int, shift: int, available_employees: List[Employee], maxShifts: int, mode: str, modifierShiftsInRow: int,employees: List[Employee], descont_employee = [], descontAllreadyAssigned = False):

    try: 
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
    except NotEnoughEmploeesException as e:
        allErrors.addError(day, shift)
        raise e
