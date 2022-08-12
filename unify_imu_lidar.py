import csv
import os
import math


'''@guoxiong 
   Caution!
   Before using this script, you need an csv file like this: 
   Time[s]      Heading   |  Time[s]      Lat          |  Time[s]        Lon
   xx.xx        xx.xxx       xx.xx        xx.xxxxxxx      xx.xx          xxx.xxxxxxx
   you can get this file from export of canoe.

   OUTPUT format: t,x,y,heading (.csv)'''
 
 
 

class imupos:
    def __init__(self):
        self.time = 0
        self.x = 0
        self.y = 0
        self.heading = 0




class gpsdata:
    def __init__ (self, list_imu):
        self.time = round(float(list_imu[3]), 3)
        self.heading = round(float(list_imu[1]), 3)
        self.lat = round(float(list_imu[4]), 7)
        self.lon = round(float(list_imu[7]), 7)
        

        

class vehiclestate:
    def __init__(self, list_lidar):
        if len(list_lidar) == 2:
            self.length = 2
            self.framenum = int(list_lidar[0])
            self.time = round(float(list_lidar[1]), 3)
        elif len(list_lidar) == 7:
            self.length = 7
            self.id = int(list_lidar[0])
            self.dx = round(0 - float(list_lidar[2]), 3)
            self.dy = round(float(list_lidar[1]), 3)
            
            


def openImuFile(imufilename):
    '''
    Description: Open csv files
    INPUT: string  [csv filename]
    OUTPUT: list  [class gpsdata]
    '''
    csv_data = csv.reader(open(imufilename, 'r'))
    content = []
    flag = 0
    for line in csv_data:
        if flag > 0:
            Gps = gpsdata(line)
            content.append(Gps)
        flag = flag + 1
    del flag
    return content




def openLidarFile(lidarfilename):
    '''
    Description: Open txt files
    INPUT: string  [txt filename]
    OUTPUT: list  [class vehiclestate]
    '''
    with open(lidarfilename, 'r') as f:
        xylist = []
        for line in f.readlines():
            line = line.strip('\n')
            b = line.split(' ')
            Vehicle = vehiclestate(b)
            xylist.append(Vehicle)
    return xylist




def mcos(degrees):
    '''
    Description: Calculate cos(theta), theta's unit is degrees
    INPUT: float  [degrees]
    OUTPUT: float 
    '''
    ans = math.cos(degrees * math.pi / 180)
    return ans




def msin(degrees):
    '''
    Description: Calculate sin(theta), theta's unit is degrees
    INPUT: float  [degrees]
    OUTPUT: float 
    '''
    ans = math.sin(degrees * math.pi / 180)
    return ans




def convertGpsToCoo(imu_data):
    '''
    Description: convert gps data to X-Y coordinates
    INPUT: list [class gpsdata]
    OUTPUT: list [class imupos]
    '''
    coo = []
    for i in range(1, len(imu_data)):
        imuTXYH = imupos()
        imuTXYH.time = imu_data[i].time
        imuTXYH.x = round((imu_data[i].lon - imu_data[1].lon) * 111000 * mcos(imu_data[i].lat), 3)
        imuTXYH.y = round((imu_data[i].lat - imu_data[1].lat) * 111000, 3)
        imuTXYH.heading = imu_data[i].heading
        coo.append(imuTXYH)
    return coo




def calDstNum(trace_data):
    '''
    Description: calculate the max num of all vehiches in the road at a moment
    INPUT: list
    OUTPUT: int
    '''
    num = []
    for i in range(len(trace_data)):
        if trace_data[i].length == 7:
            num.append(trace_data[i].id)
    numset = list(set(num))
    return len(numset)




def synCalXY(imu, lidar):
    '''
    Description: sync data from imu and lidar by timestramp
    INPUT: list
    OUTPUT: list
    '''
    dst = []
    for i in range(len(lidar)):
        posTXYH = imupos()
        if lidar[i].length == 7:
            a = 0
            # find lidar timestramp
            while (lidar[i - a].length == 7):
                a = a + 1
            t = lidar[i - a].time
            # find imu timestramp
            b = 2
            while (abs(t - imu[int(t * 100 - b)].time) > 0.01):
                b = b - 1
                if b == -2:
                    break
            posTXYH.time = t
            index = int(t * 100 - b)
            # Calulate x, y distance between imu and other vehicles
            Dx = lidar[i].dx * mcos(imu[index].heading) + lidar[i].dy * msin(imu[index].heading)
            Dy = lidar[i].dy * mcos(imu[index].heading) - lidar[i].dx * msin(imu[index].heading)
            posTXYH.x = round(imu[index].x + Dx, 3)
            posTXYH.y = round(imu[index].y + Dy, 3)
            posTXYH.heading = imu[index].heading
            dst.append(posTXYH)
    return dst
                
  
  
  
def setOffset(track, x_offset, y_offset):
    '''
    Description: Calculate x, y after adding x_offset, y_offset
    INPUT: list
    OUTPUT: list 
    '''
    for i in range(len(track)):
        track[i].x = round(track[i].x + x_offset, 3)
        track[i].y = round(track[i].y + y_offset, 3)
    return track
      
 
 
 
def saveFile(vehicle_information, csv_filename):
    '''
    Description: Save data as csv
    INPUT: list
    OUTPUT: csv 
    '''
    list_to_write = []
    for i in range(0, len(vehicle_information)):
        list_to_add = []
        list_to_add.append(vehicle_information[i].time)
        list_to_add.append(vehicle_information[i].x)
        list_to_add.append(vehicle_information[i].y)
        list_to_add.append(vehicle_information[i].heading)
        list_to_write.append(list_to_add)
        
    csv_out = csv.writer(open(csv_filename, 'w+'), dialect = 'excel')
    for line in list_to_write:
        csv_out.writerow(line)
        print(line)

 
 
        
if __name__ == "__main__":
    
    # set begining point offset
    start_x_offset = 646
    start_y_offset = 582
    
    csv_file = 'sourcefile/simulation_imu.csv'
    lidar_file = 'sourcefile/aosen1.txt'
    output_lidar_file = 'generatedfiles/vehicle_pos.csv'
    output_imu_file = 'generatedfiles/imu_pos.csv'
    
    imucsv = openImuFile(csv_file)
    imu_xyh = convertGpsToCoo(imucsv)
    
    lidar_idxy = openLidarFile(lidar_file)
    veh_num = calDstNum(lidar_idxy)
    
    txyh = synCalXY(imu_xyh, lidar_idxy) 

    veh_track = setOffset(txyh, start_x_offset, start_y_offset)
    imu_track = setOffset(imu_xyh, start_x_offset, start_y_offset)
    
    saveFile(veh_track, output_lidar_file)
    saveFile(imu_track, output_imu_file)
    
    
    
        
        
        
        
        
        
        