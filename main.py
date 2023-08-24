from typing import List, Tuple
 
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

# Generate the schedule
def generate_schedule(employees: list[Employee]) -> list[list[tuple[str, int]]]:
    schedule = [[] for _ in range(7)]
    num_shifts = {employee.name: 0 for employee in employees}
    # Generate the of days (range)
    for day in range(3):
        # Generate the shifts (range)
        for shift in [1, 2, 3]:
            # Generate the employees (list comprehension)
            available_employees = [employee for employee in employees if shift in employee.possibleShifts[day] if shift not in employee.offShifts]
            # Generate the contract employees (list comprehension)
            contract_employees = [employee for employee in available_employees if employee.contract]
            # Assign the contract employees
            for employee in contract_employees:
                schedule[day].append((employee.name, shift))
                num_shifts[employee.name] += 1
                available_employees.remove(employee)
            # Sort the available employees by the number of shifts they have
            #TODO change rules, that schedule will prioritize epmloyees to get 3-5 shifts in row
            available_employees.sort(key=lambda employee: num_shifts[employee.name])
            coordinator = next((employee for employee in available_employees if employee.coordinator), None)
            # Assign the coordinator (no more than one per shift)
            if coordinator:
                schedule[day].append((coordinator.name, shift))
                num_shifts[coordinator.name] += 1
                continue
            # Assign the descont employee (at least one per shift)
            descont_employee = next((employee for employee in available_employees if employee.descont), None)
            if descont_employee:
                schedule[day].append((descont_employee.name, shift))
                num_shifts[descont_employee.name] += 1
                available_employees.remove(descont_employee)
            # Assign the rest of the employees
            while len([x for x in schedule[day] if x[1] == shift]) < 3:
                if not available_employees:
                    break
                employee = available_employees.pop(0)
                schedule[day].append((employee.name, shift))
                num_shifts[employee.name] += 1
            # If there are not enough employees, generate the schedule again
            if len([x for x in schedule[day] if x[1] == shift]) < 2:
                #TODO Recuration is not working properly, need to be fixed
                return generate_schedule(employees)
        #At least 2 shifts between work
        if day != 0:
            prevDaySchedule = [employee for employee in schedule][day-1]
            for n in range(len(prevDaySchedule)):
                if prevDaySchedule[n][1] == 3:
                    for employee in employees:
                        if employee.name == prevDaySchedule[n][0]:
                            employee.offShifts.clear()
                            employee.offShifts.append(1)
                            employee.offShifts.append(2)
                            print(employee.name, employee.offShifts)
                elif prevDaySchedule[n][1] == 2:
                    for employee in employees:
                        if employee.name == prevDaySchedule[n][0]:
                            employee.offShifts.clear()
                            employee.offShifts.append(1)
                            print(employee.name, employee.offShifts)
                else:
                    for employee in employees:
                        if employee.name == prevDaySchedule[n][0]:
                            employee.offShifts.clear()
                            print(employee.name, employee.offShifts)


    return schedule
 

PJ = Employee("P", "J", [[2],[2],[2],[2],[2],[2],[2]], True,False,False)
KM = Employee("K", "M", [[2],[3],[2],[2],[2],[1,2],[1,2]], False,False,False)
KM1 = Employee("K", "M", [[3],[3],[3],[3],[3],[3],[3]], True,False,True)
DS = Employee("D", "S", [[2,3],[3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3]], True,False,False)
MB = Employee("M", "B", [[2],[3],[2],[2],[2],[2,3],[2,3]], True,False,False)
KT = Employee("K", "T", [[2],[2],[2],[2],[2],[2],[2]], True,False,True)
MM = Employee("M", "M", [[2],[2],[2],[2],[2,3],[1,2,3],[1,2,3]], False,False,False)
BT = Employee("B", "T", [[3],[3],[3],[3],[3],[3],[3]],False,False,False)
KD = Employee("K", "D", [[2],[2],[3],[3],[3],[1],[1]],True,False,False)
GW = Employee("G", "W", [[2],[2],[2],[3],[3],[1],[1]], True,False,False)
JG = Employee("J", "G", [[2,3],[3],[2],[3],[2,3],[2,3],[1]], True,False,False)
FJ = Employee("F", "J", [[1],[1],[1],[1],[1],[],[]], False,True,False)
KC = Employee("K", "C", [[3],[2],[3],[2],[3],[3],[1]], True,False,False)

employees = [PJ, KM, KM1, DS, MB, KT, MM, BT, KD, GW, JG, FJ, KC]

# Generate the schedule
schedule = generate_schedule(employees)

# Print the schedule
for day in range(7):
    print(f"Day {day + 1}:")
    for employee_name, shift in schedule[day]:
        print(f"  Shift {shift}: {employee_name}")
