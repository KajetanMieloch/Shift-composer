from typing import List
import json

# Employee class
class Employee:
    def __init__(self, name: str, surename: str, id: int, day0 :int, possibleShifts: List[List[int]], descont: bool, coordinator: bool, contract: bool,):
        self.name = name
        self.surename = surename
        self.id = id
        self.day0 = day0
        self.possibleShifts = possibleShifts   
        self.descont = descont
        self.coordinator = coordinator
        self.contract = contract
        self.offShifts = []
        self.shiftsInRow = 0
        self.hadShift = False
        self.doNotAssign = False
        self.hoursInTotal = 0
        self.workedDays = []
        
        self.setOffShiftsBasedOnDay0()
    
    def setOffShiftsBasedOnDay0(self):
        if self.day0 == 2:
            self.offShifts = [1]
        elif self.day0 == 3:
            self.offShifts = [1,2]

with open('employees.json', 'r') as f:
    data = json.load(f)

#Define employees
def defineEmployees():
    employees = []
    for employeeData in data:
        employee = Employee(
            employeeData['first_name'],
            employeeData['last_name'],
            employeeData['id'],
            employeeData['day0'],
            employeeData['schedule'],
            employeeData['is_manager'],
            employeeData['is_full_time'],
            employeeData['is_part_time']
        )
        employees.append(employee)
    return employees
