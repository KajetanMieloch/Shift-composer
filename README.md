# Shift Composer

## Description
Shift Composer is a program that takes the disposition of every employee and generates a schedule. The program is compatible with a 3-shift day of work, with a minimum of 1 shift break between shifts.

## Configuration
The program can be configured using the `config.ini` file, where you can specify the number of days for which the schedule should be generated.

## Usage
To use the program, you need to modify `Employee` objects for each employee in `Employee.json`.
Attributes:
- `name`: The employee's name.
- `surname`: The employee's surname.
- `id`: The employee's ID.
- `day0`: The last shift in the previous month that the employee had.
- `possibleShifts`: A list of all shifts that the employee may have.
- `descont`: A boolean flag to determine if the employee has central training. At least one employee with this flag set to `True` must be on a shift.
- `coordinator`: A boolean flag to determine if the employee is a coordinator. A coordinator is assigned first and if they have a disposition, they must be on a shift. If there is a coordinator on shift, no one else has a shift with them.
- `contract`: A boolean flag to determine if the employee has a fixed schedule. They are assigned first and if they have a disposition, they must be on a shift.
#
For Python 3.7 and 3.8, add:

`from __future__ import annotations`
