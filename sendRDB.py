'''@guoxiong'''
import socket
import time
import csv
from struct import *
import os
import math
import RdbMessage.Message



class objectstate:
    def __init__(self):
        self.id = 1
        self.type = 1
        self.name = 'Ego'
        self.posi = [0, 0, 0]
        self.radi = [0, 0, 0]
        self.spee = [0, 0, 0]
        
        
        
class vehiclepos:
    def __init__(self, csv_list):
        self.time = round(float(csv_list[0]), 3)
        self.x = round(float(csv_list[1]), 3)
        self.y = round(float(csv_list[2]), 3)
        self.heading = round(float(csv_list[3]), 3)
  
  
  
def packRDB(objst = objectstate()):
    print objst.posi
    # print 'add'
    with open('cachefiles/./pathshape_coord.txt', 'a') as f:
        f.write(str(objst.posi[0]) + ',' + str(objst.posi[1]) + ' ')
    # p(objst.posi[0], objst.posi[1])
    return RdbMessage.Message.ObjectState(objst.id, 1, objst.name, objst.posi, objst.radi, 1, 1, objst.spee)




def readVehicleState(filename):
    csv_data = csv.reader(open(filename, 'r'))
    state = []
    for line in csv_data:
        vehicle_txyh = vehiclepos(line)
        state.append(vehicle_txyh)
    return state




def degrees2rad(deg):
    rad = round(deg/180, 3)*math.pi
    return -(rad - math.pi / 2)




def gatherData(imu_data, lidar_data):
    t = 0.1
    imu_list1 = []
    imu_list2 = []
    imu_list1.append(imu_data[0])
    imu_list2.append(imu_list1)
    for i in range(0, len(imu_data)):
        imu_list1 = []
        # finding imu data by period [100ms]
        if (abs(imu_data[i].time - t) < 0.01):
            imu_list1.append(imu_data[i])
            imu_list2.append(imu_list1)
            t = t + 0.1
    # matching lidar data with imu data
    for j in range(0, len(lidar_data)):
        imu_list2[int(round(lidar_data[j].time, 1) * 10)].append(lidar_data[j])
    return imu_list2
 
 

def calMaxVehicleNum(data):
    max_num = 0
    for i in range(len(data)):
        print(data[i])
        if len(data[i]) > max_num:
            max_num = len(data[i])
    return max_num



def stroeDataToBagList(datatostroe):
    object_bag = []     # use for stroing vehicle state data 
    for i in range(len(datatostroe)):
        veh_stat = []
        for j in range(len(datatostroe[i])):
            veh_sta = objectstate()
            veh_sta.id = j + 1
            # print vehicle_state[i][0], vehicle_state[i][1]
            veh_sta.posi = [datatostroe[i][j].x, datatostroe[i][j].y, 0]
            # pos_z[i] - z_init]                    
            veh_sta.radi = [degrees2rad(datatostroe[i][j].heading), 0, 0]  # ang_p[i], ang_r[i]]
            veh_sta.spee = [0, 0, 0]
            veh_stat.append(veh_sta)
        object_bag.append(veh_stat)
    return object_bag


    

if __name__ == "__main__":
    # data init
    csv_imu = 'generatedfiles/imu_pos.csv'
    csv_vehiche = 'generatedfiles/vehicle_pos.csv'
    
    imu_state = readVehicleState(csv_imu)
    # print(len(imu_state))
    
    vehicle_state = readVehicleState(csv_vehiche)
    # print(len(vehicle_state))
    
    mix_data = gatherData(imu_state, vehicle_state)
    
    max_vehicle_num = calMaxVehicleNum(mix_data)
    
    data_bag = stroeDataToBagList(mix_data)

    # pack data and send to host port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    port = 48191 
    steplength = 0.1
    stop_state = objectstate()
    
    for i in range(len(data_bag)):
        t1 = time.time()
        for j in range(max_vehicle_num):
            if j < len(data_bag[i]):
                RDBmsg = RdbMessage.Message.Start()
                RDBmsg += packRDB(data_bag[i][j])
                RDBmsg += RdbMessage.Message.Trigger(i, steplength)
                RDBmsg += RdbMessage.Message.End()
                RDBmsg = RdbMessage.Message.Generate(RDBmsg, i, steplength)
            else:
                stop_state.id = j + 1
                RDBmsg = RdbMessage.Message.Start()
                RDBmsg += packRDB(stop_state)
                RDBmsg += RdbMessage.Message.Trigger(i, steplength)
                RDBmsg += RdbMessage.Message.End()
                RDBmsg = RdbMessage.Message.Generate(RDBmsg, i, steplength)
            s.sendto(RDBmsg, (('127.0.0.1', port)))
        t2 = time.time()
        ts = t2 - t1 
        time.sleep(steplength - ts)
            
    s.close()

