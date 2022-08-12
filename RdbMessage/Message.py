# from PkgSize import *
from struct import *

# Create a Char with Size of "CharSize" Bytes
def Char_Size(msg, Size = 32):
    msg_add = pack('L', 0)
    if Size == 32:
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg = msg[0:32]
    elif Size == 64:
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg += msg_add
        msg = msg[0:64]
    
    return msg

# Header of RDB Message
def Header(Size, Step, StepLength):
    msg = pack('H', 35712)
    msg += pack('H', 256)
    msg += pack('I', 24)
    msg += pack('I', Size)
    msg += pack('I', Step)
    msg += pack('d', Step * StepLength)

    return msg

# Entry of RDB Message
def Entry(pkgID, DataSize = 0, ElementSize = 0, flag = 0):
    msg = pack('I', 16)
    msg += pack('I', DataSize)
    msg += pack('I', ElementSize)
    msg += pack('H', pkgID)
    msg += pack('H', flag)

    return msg

# RDB Message, Package ID = 1
def Start():
    return Entry(1)

# RDB Message, Package ID = 2
def End():
    return Entry(2)

# RDB Message, Package ID = 9
def ObjectState(ID, Type, Name, Point, Radius, CfgModel, flag = 0, speed = [0, 0, 0], palstance = 0):
    msg = pack('I', ID)
    msg += pack('H', Type * 256 + 1)
    msg += pack('H', 7)
    msg += Char_Size(Name)
    msg += pack('f', 4.3)
    msg += pack('f', 1.776)
    msg += pack('f', 1.423)
    msg += pack('f', 1.317)
    msg += pack('f', 0)
    msg += pack('f', 0)
    msg += pack('d', Point[0])
    msg += pack('d', Point[1])
    if len(Point) == 3:
        msg += pack('d', Point[2])
    else:
        msg += pack('d', 0)
    msg += pack('f', Radius[0])
    msg += pack('f', Radius[1])
    if len(Radius) == 3:
        msg += pack('f', Radius[2])
    else:
        msg += pack('d', 0)
    msg += pack('H', 513)
    msg += pack('H', 0)
    msg += pack('I', 0)
    msg += pack('H', 3)
    msg += pack('h', CfgModel)
    if flag:
        msg += pack('d', speed[0])
        msg += pack('d', speed[1])
        msg += pack('d', speed[2])
        msg += pack('f', palstance)
        msg += pack('f', 0)
        msg += pack('f', 0)
        msg += pack('H', 513)
        msg += pack('H', 0)
        msg += pack('d', 0)
        msg += pack('d', 0)
        msg += pack('d', 0)
        msg += pack('f', 0)
        msg += pack('f', 0)
        msg += pack('f', 0)
        msg += pack('H', 513)
        msg += pack('H', 0)
        msg += pack('f', 0)
        msg += pack('I', 0)

    msg = Entry(9, len(msg), len(msg), flag) + msg

    return msg

# RDB Message, Package ID = 11
def VehicleSetup(VehID, Mass, WheelBase):
    msg = pack('I', VehID)
    msg += pack('f', Mass)
    msg += pack('f', WheelBase)
    msg += pack('i', 0)

    msg = Entry(11, len(msg), len(msg)) + msg

    return msg

# RDB Message, Package ID = 25
def Trigger(Step, StepLength):
    msg = pack('f', StepLength)
    msg += pack('I', Step)
    msg += pack('H', 1)
    msg += pack('H', 0)

    msg = Entry(25, len(msg), len(msg)) + msg

    return msg

# RDB Message, Pakcage ID = 27
def TrafficLight(ID, State, flag = 0, CtrlID = 0, Phase = 0):
    msg = pack('i', ID)
    msg += pack('f', State)
    msg += pack('I', 65535)
    if flag == 1:
        msg += pack('i', CtrlID)
        msg += pack('f', 90)
        msg += pack('H', 3)
        msg += pack('I', 8 * 3)
        msg += pack('f', 0.3)
        msg += pack('H', 3 * 256)
        msg += pack('H', 0)
        msg += pack('f', 0.3)
        msg += pack('H', 3 * 256)
        msg += pack('H', 0)
        msg += pack('f', 0.4)
        msg += pack('H', 5 * 256)
        msg += pack('H', 0)

    msg = Entry(27, len(msg), len(msg), flag) + msg

    return msg

# RDB Message, Package ID = 28
def Sync(Step, StepLength):
    return ''

# RDB Message, Package ID = 33
def SCP(ScpMsg):
    msg = pack('H', 256)
    msg += pack('H', 0)
    msg += Char_Size('sender', 64)
    msg += Char_Size('receiver', 64)
    msg += pack('I', len(ScpMsg))
    msg += ScpMsg

    msg = Entry(33, len(msg), len(msg)) + msg

    return msg

# Generate RDB Message
def Generate(RdbMsg, Step, StepLength):
    msg = Header(len(RdbMsg), Step, StepLength)
    msg += RdbMsg

    return msg