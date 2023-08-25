from typing import List, Tuple


#Number of days in schedule
days = 1



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

# Generate the schedule
def generate_schedule(employees: list[Employee]) -> list[list[tuple[str, int]]]:
    schedule = [[] for _ in range(days)]
    
    # Generate the of days (range)
    for day in range(days):
        # Generate the shifts (range)
        for shift in [1, 2, 3]:
            # Generate the employees (list comprehension)
            available_employees = [employee for employee in employees if shift in employee.possibleShifts[day] if shift not in employee.offShifts]
            # Generate the contract employees (list comprehension)
            contract_employees = [employee for employee in available_employees if employee.contract]
            
            contractEmployOnShift = False
            
            # Assign the contract employees
            for employee in contract_employees:
                schedule[day].append((employee.name, shift))
                available_employees.remove(employee)
                contractEmployOnShift = True
            
           
            coordinator = next((employee for employee in available_employees if employee.coordinator), None)
            
            # Assign the coordinator (no more than one per shift)  
            if coordinator:
                schedule[day].append((coordinator.name, shift))
                continue
            
            #Assign the descont employee (at least one per shift)
            descont_employee = [employee for employee in available_employees if employee.descont]
            #Sort the list of descont employees by shiftsInRow
            descont_employee.sort(key=lambda employee: employee.shiftsInRow, reverse=True)
            if descont_employee is not None and not contractEmployOnShift:
                schedule[day].append((descont_employee[0].name, shift))
                available_employees.remove(descont_employee[0])
                descont_employee[0].shiftsInRow += 1
                #Number of shifts in row is reseted to 0
                if descont_employee[0].shiftsInRow == 5:
                    descont_employee[0].shiftsInRow = -1
            
            # Assign the rest of the employees
            available_employees.sort(key=lambda employee: employee.shiftsInRow, reverse=True)
          

            while len([x for x in schedule[day] if x[1] == shift]) < 3:
                if not available_employees:
                    break
                employee = available_employees.pop(0)
                schedule[day].append((employee.name, shift))
                employee.shiftsInRow += 1
                #Number of shifts in row is reseted to 0
                if employee.shiftsInRow == 5:
                    employee.shiftsInRow = -1
                
            #If there is less than 2 employees on shift, then recurency is called
            if len([x for x in schedule[day] if x[1] == shift]) < 2:
                print("Recurency")
                #TDOO: Recurency is called and the shift is changed.

        if day != 0:
            prevDaySchedule = [employee for employee in schedule][day-1]
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
 

PJ = Employee("Same2.0", "J", [[]], True,False,False)
KM2 = Employee("Same1 - Brutusia", "M", [[1]], True,False,False)
KM3 = Employee("Same2, weekend 1,2 - Gosia", "M", [[]], True,False,False)
KM1 = Employee("Same2.2 - UmowaPraca", "M", [[2]], True,False,True)
DS = Employee("Same3.0", "S", [[3]], True,False,False)
MB = Employee("Same3.1", "B", [[3]], True,False,False)
KC = Employee("Same3.3 - Kasia", "C", [[1]], True,False,False)
BM = Employee("Same3.4 - Basia", "M", [[1]], True,False,False)
KT = Employee("same3.2 - UmowaPraca", "T", [[3]], True,False,True)
FJ = Employee("Koordynator", "J", [[]], False,True,False)


employees = [PJ, KM1, DS, MB, KT, FJ, KC, BM, KM2, KM3]

# Generate the schedule
schedule = generate_schedule(employees)

# Print the schedule
for day in range(days):
    print(f"Day {day + 1}:")
    for employee_name, shift in schedule[day]:
        print(f"  Shift {shift}: {employee_name}")
