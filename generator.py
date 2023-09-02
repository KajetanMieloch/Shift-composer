from generatorResources import *

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
                    schedule[day].append((coordinator.name, shift, coordinator.id, coordinator.surename))
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
                    schedule[day].append((employee.name, shift, employee.id, employee.surename))
                    available_employees.remove(employee)
                    descontAllreadyAssigned = True

                #Assign the descont employee (at least one per shift)
                if descont_employee:
                    assignDescontEmployee(schedule, day, shift, available_employees, descont_employee, modifierShiftsInRow)

                #If there is no descont employee, then try delete previous shift descont employee
                elif not descont_employee:
                    reasignEmployee(schedule, day, shift, available_employees, maxShifts, "descont",modifierShiftsInRow, employees, descont_employee, descontAllreadyAssigned)
                    
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
                                schedule[day].append((employee.name, shift, employee.id, employee.surename))
                                available_employees.remove(employee)
                                shiftsInRow(employee, day, modifierShiftsInRow)
                                break
                    #If there is no nonDescontPriority, then descont employee is assigned first
                    #but if employee has doNotAssign set to True, then he is not assigned
                    elif iterationOfDescontEmployee <=3 and shift <=3:
                        for employee in available_employees:
                            if employee.doNotAssign == False:
                                schedule[day].append((employee.name, shift, employee.id, employee.surename))
                                available_employees.remove(employee)
                                shiftsInRow(employee, day, modifierShiftsInRow)
                                break

                    #Else, employee is assigned by order
                    else:
                        if employee.doNotAssign == False:                        
                            if assignEmployeesByOrder(available_employees, schedule, day, shift ,0, maxShifts, modifierShiftsInRow, employees):
                                break   
                        else:
                            if assignEmployeesByOrder(available_employees, schedule, day, shift ,1, maxShifts, modifierShiftsInRow, employees):
                                break

                #TODO Program a recurency, that will figure out what to do if there is no more employees to assign
                #If there is less than 2 employees on shift, then recurency is called
                if len([x for x in schedule[day] if x[1] == shift]) < 2:
                    raise NotEnoughEmploeesException("Not enough employees on shift" + str(shift) + " on day " + str(day+1))

            assignEmployeeOffShifts(schedule, day, employees)
    
    #If there is exeption, then return False
    except NotEnoughEmploeesException as e:
        allErrors.addError(day, shift)
        return False

    return schedule
