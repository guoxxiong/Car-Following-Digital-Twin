import random

class VehicleType:
    def __init__(self):
        Name = ''
        Length = 5.000
        Offset = 0.000
        Distance = 0.000

Name = ['Audi_A3_2009', 'Audi_A4_2009', 'Audi_A6_2007', 'Audi_A6_2010', 'Audi_A8L_2008', 'Audi_Q5_2008', 'Audi_S5_2009', 'MAN_TGL_2009', 'MB_S_2007', 'MB_S_2009', 'Nissan_Z350_2007', 'Smart_2007', 'MB_Sprinter_2007', 'MB_Actors_2007', 'VW_Golf_2010', 'VW_Golf_2012', 'VW_PassatVariant_2011', 'VW_Tiguan_2012', 'VW_Touareg_2010', 'VW_Touran_2009', 'Kawasaki_ZX_9R']
Length = [4.300, 4.674, 4.796, 4.924, 5.179, 4.646, 4.639, 6.440, 5.032, 5.118, 4.322, 2.514, 5.666, 6.654, 4.157, 4.221, 4.749, 4.433, 4.790, 4.415, 2.043]
Offset = [1.766, 1.780, 1.806, 1.872, 1.908, 1.926, 1.842, 2.558, 1.820, 1.886, 1.896, 1.480, 1.932, 2.150, 1.718, 1.762, 1.798, 1.784, 1.952, 1.806, 0.650]
IdList = [5, 14, 20, 25, 31, 38, 47, 53, 58, 63, 69, 74, 79, 84, 89, 94, 99, 104, 109, 114, 118]
TypeList = []

for i in range(len(Name)):
    TypeList.append(VehicleType())
    TypeList[i].Name = Name[i]
    TypeList[i].Length = Length[i]
    TypeList[i].Offset = Offset[i]
    TypeList[i].Distance = TypeList[i].Length / 2 + TypeList[i].Offset

def TypeDistance(TypeID):
    for i in range(len(Name)):
        if TypeID < IdList[i]:
            return TypeList[i].Distance
    return 0

def TypeName(TypeID):
    for i in range(len(Name)):
        if TypeID < IdList[i]:
            return TypeList[i].Name
    return False

def TypeRandom():
    ID = -1
    while ID < 0 or ID == 47 or ID == 79:
        ID = random.randint(0, 113)
    return ID
