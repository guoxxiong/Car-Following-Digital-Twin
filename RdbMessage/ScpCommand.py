import random

Ped_Shape = {'fped_07':['sk_chinese_old_woman','sk_female_casual_2','sk_female_casual_3','sk_female_casual_9','sk_female_suit_2'],'cped_07':['sk_male_child_1','sk_male_child_3','female_teen_1','female_teen_3','male_teen_1','male_teen_3','sk_ariel','sk_kim'],'mped_07':['sk_emt_1','sk_male_casual_1','sk_male_casual_11','sk_male_casual_14','sk_male_casual_16','sk_male_casual_2','sk_male_casual_9','sk_male_suit_4','sk_rex_jeans']}
Bike_Shape = {'fped_bike':['sk_female_casual_1','sk_female_casual_8','sk_female_casual_4','sk_female_suit_5'],'mped_bike':['sk_cameraman','sk_male_casual_10','sk_male_casual_13','sk_male_casual_15','sk_male_casual_14','sk_male_casual_5','sk_male_casual_9','sk_male_suit_1','sk_pkk_fighter_1']}
Gesture_Type = ['', '', '', '', '', '', '','arm_l_3s_wave1','arm_l_3s_you_know5','arm_l_2s_i_dont_know3','arm_l_3s2c_chop']

def Create(ID, name, category):
    msg = '<Player id="'
    msg += str(ID)
    msg += '" name="'
    msg += name
    msg += '"><Create category="'
    if category == 'vehicle':
        msg += 'vehicle'
    else:
        msg += 'pedestrian'
    msg += '" '
    if category == 'vehicle':
        msg += 'adaptDriverToVehicleType="true"'
    elif category == 'pedestrian':
        msg += 'type="'
        Ped_Type = random.choice(list(Ped_Shape.keys()))
        msg += Ped_Type
        msg += '" model="'
        Ped_Model = random.choice(Ped_Shape[Ped_Type])
        msg += Ped_Model
        msg += '"'
    elif category == 'bicycle':
        msg += 'type="'
        Bike_Type = random.choice(list(Bike_Shape.keys()))
        msg += Bike_Type
        msg += '" model="'
        Bike_Model = random.choice(Bike_Shape[Bike_Type])
        msg += Bike_Model
        msg += '"'
    msg += '/></Player>'
    return msg

def DeleteVeh(ID):
    msg = '<Player id="'
    msg += str(ID)
    msg += '"><Delete/></Player>'

    return msg

def TrafficLight(CtrlID, Phase):
    msg = '<TrafficLight><SetPhase syncJunction="true" ctrlId="'
    msg += str(CtrlID)
    msg += '" phase="'
    msg += Phase
    msg += '" fadeTime="0.0"/></TrafficLight>'

    return msg 

def Restart():
    return "<SimCtrl><Restart/></SimCtrl>"

def Signals(ID, Signal):
    msg = '<Player id="'
    msg += str(ID)
    msg += '"><Light type="brake" state="'
    if Signal >= 8:
        msg += 'on'
        Signal -= 8
    else:
        msg += 'off'
    
    msg += '"/><Light type="indicator left" state="'
    if Signal >= 2:
        msg += 'on'
        Signal -= 2
    else:
        msg += 'off'
    
    msg += '"/><Light type="indicator right" state="'
    if Signal >= 1:
        msg += 'on'
        Signal -= 1
    else:
        msg += 'off'
    
    msg += '"/></Player>'

    return msg

def ActionMotion(name, move = 1, character = 'pedestrian', motion = 'walk'):
    msg = '<Traffic><ActionMotion actor="'
    msg += name
    msg += '" move="'
    if move == 2:
        msg += motion
    else:
        if character == 'pedestrian':
            msg += 'stand'
        elif character == 'bicycle':
            msg += 'still'
    msg += '" force="true" delayTime="0.00"/><ActionGesture actor="'
    msg += name
    msg += '" gestureType="'
    msg += random.choice(Gesture_Type)
    msg += '" delayTime="'
    msg += str(random.random() * 10)
    msg += '"/></Traffic>'
    
    return msg
