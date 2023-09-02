from typing import List
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

#Define employees
def defineEmployees(n = 0):
    FJ = Employee("Filip", "J",1,n, [[1],[1],[1],[1],[1],[],[],[1],[1],[1],[1],[1],[],[],[1],[1],[1],[1],[1],[],[],[1],[1],[1],[1],[1],[],[],[1],[1]], False,True,False)
    KM = Employee("Kacper", "M",2,n, [[2],[2],[2],[2],[],[],[],[],[2],[2],[],[],[2],[2],[2],[],[2],[],[],[2],[2],[2],[2],[2],[],[],[2],[2],[2],[]], True,False,True)
    MB = Employee("Maks", "B",3,n, [[2],[2],[],[],[2,3],[1,2],[1,2],[],[],[],[],[],[1],[],[3],[3],[2,3],[2],[3],[2],[2,3],[3],[],[],[],[],[2],[3],[2],[2]], True,False,False)
    KT = Employee("Krystian", "T",4,n, [[3],[],[],[3],[3],[3],[3],[3],[],[],[3],[3],[3],[3],[3],[],[],[],[],[],[],[],[],[],[3],[3],[3],[3],[3],[]], True,False,True)
    KD = Employee("Kamil", "M",5,n, [[3],[2],[3],[2],[],[],[],[],[],[],[],[],[],[2,3],[2,3],[2,3],[3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[],[],[],[]], True,False,False)
    GW = Employee("Grzegorz", "W",6,n, [[],[],[3],[2],[2],[1],[1],[2],[],[],[2],[2],[1],[],[2],[2],[3],[],[2],[1],[1],[],[],[],[],[],[1],[1],[2],[]], True,False,False)
    KM2 = Employee("Kajetan", "M",7,n, [[2,3],[2],[2],[2,3],[2,3],[1,2],[2],[],[],[],[],[],[],[1,2],[3],[2],[2],[2],[2,3],[1,2],[1,2],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[2,3]], False,False,False)
    PJ = Employee("Piotr", "J",8,n, [[3],[3],[3],[2,3],[2,3],[3],[3],[3],[3],[2,3],[3],[3],[3],[3],[3],[3],[2,3],[2],[2,3],[2],[],[],[],[],[],[],[],[3],[2],[2]], True,False,False)
    KC = Employee("Kasia", "C",9,n, [[3],[3],[],[3],[],[],[],[3],[2],[],[],[],[],[3],[],[3],[],[],[3],[],[],[],[3],[2],[3],[3],[2],[3],[3],[]], True,False,False)
    DS = Employee("Damian", "S",10,n, [[],[2,3],[3],[2,3],[2,3],[],[1,2,3],[2,3],[2,3],[],[2],[2,3],[1,2,3],[1,2,3],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[],[2,3],[2,3],[2,3],[2,3],[3],[1,3],[3],[2]], True,False,False)
    JG = Employee("Jakub", "G",9,n, [[2,3],[],[3],[2,3],[3],[1,2],[1],[2,3],[2,3],[2,3],[2,3],[2,3],[1,2,3],[1,2,3],[2,3],[],[2,3],[2,3],[2,3],[1,2,3],[1],[2],[2],[2,3],[3],[3],[1,2,3],[1,2,3],[2,3],[2,3]], True,False,False)
    MM = Employee("Mateusz", "M",12,n, [[2,3],[2],[2],[2,3],[],[1],[2],[3],[2,3],[3],[],[2],[],[],[],[2],[2],[2],[],[3],[2,3],[2,3],[2,3],[2,3],[2,3],[1],[1],[],[2],[2]], False,False,False)
        
    return [FJ, KM, MB, KT, KD, GW, KM2, PJ, KC, DS, JG, MM]