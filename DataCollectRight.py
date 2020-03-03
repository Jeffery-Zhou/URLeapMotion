# -*- coding: UTF-8 -*-
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# import for LeapMotion
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Vector

# import for UR3
import urx
import math
from math import pi
# create thread to execute the two UR3 simualtanious
import threading
from threading import Thread
import time

class printer:   
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def okb(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.OKBLUE + t + ' ' + text + cls.ENDC)

    @classmethod
    def okg(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.OKGREEN + t + ' ' + text + cls.ENDC)

    @classmethod
    def warn(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.WARNING + t + ' ' + text + cls.ENDC)

    @classmethod
    def header(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.HEADER + t + ' ' + text + cls.ENDC)        

    @classmethod
    def fail(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.FAIL + t + ' ' + text + cls.ENDC)  

    @classmethod
    def bold(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.BOLD + t + ' ' + text + cls.ENDC)          

    @classmethod
    def underline(cls, text):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(cls.UNDERLINE + t + ' ' + text + cls.ENDC)            


class UR3:
    Left_UR3_IP = "158.132.172.193" 
    Right_UR3_IP = "158.132.172.214"

    @classmethod
    def connectRightUR(cls):
        rob = urx.Robot(cls.Right_UR3_IP)
        rob.set_tcp((0,0,0,0,0,0))
        rob.set_payload(1.5, (0,0,0))
        time.sleep(0.2)
        printer.header("==================== Right UR3 connected. ====================")
        # intial_joints = [-0.0482409636126917, -0.748549763356344, 1.3524250984191895, -3.763566795979635, -1.5582435766803187, 9.371355835591451] 
        # intial_joints = [0.5243943950121863, -0.07798659231070386, 0.25202923769305685, -0.06403291554008664, -3.094951547164568, 0.017947641504043658]
        intial_joints = [0.10511700809001923, -2.754655663167135, -1.0462172667132776, 0.6226247549057007, -4.769015494977133, -0.06416160265077764] 
        # [0.039932187646627426, -2.416210476552145, -1.6089499632464808, 0.8271387815475464, -4.680840078984396, -0.06411344209779912] 
        # [0.10511700809001923, -2.754655663167135, -1.0462172667132776, 0.6226247549057007, -4.769015494977133, -0.06416160265077764]         
        rob.movej(intial_joints, acc= 0.25, vel=0.15)
        printer.header("==================== Right UR3 finished initial setting. ====================")
        return rob

    @classmethod
    def connectLeftUR(cls):
        rob = urx.Robot(cls.Left_UR3_IP)
        rob.set_tcp((0,0,0,0,0,0))
        rob.set_payload(1.5, (0,0,0))
        time.sleep(0.2)
        printer.header("==================== Left UR3 connected. ====================")
        intial_joints = [-0.03303844133485967, -0.4258616606341761, 1.2580962181091309, -3.8896873633014124, -1.6458943525897425, 9.371907297764913] 
        # [-0.027399841939107716, -0.9967621008502405, 1.7950401306152344, -3.9452269713031214, -1.5623214880572718, 9.370444122944967]
        rob.movej(intial_joints, acc= 0.3, vel=0.2)
        printer.header("==================== Left UR3 finished initial setting. ====================")
        return rob

    @classmethod 
    def moveRightPose(cls, rob, pos_displace, angle = 0.0):
        try:
            l = 0.02
            v = 0.1    # velocity
            a = 0.2     # acceleration
            pose = rob.getl()
            t = rob.get_pose() # transformation from Base to TCP

            # t0 = rob.get_pose()
            print("Right UR: the current pose is : %s"  % pose)
            # print("Translate in -x and rotate")
            # t0.orient.rotate_zb(pi/18)
            for i in range(3):
                if i == 0: # in / out
                    t.pos[i] += pos_displace[i]/3.0
                elif i == 1: # up / down
                    t.pos[i] += pos_displace[i]/1.5
                else:   # left / right
                    t.pos[i] += pos_displace[i]/2.0
            print("Right UR: the target pose is %s with a displacement %s" % (t.pos, pos_displace))
            # rob.movel(pose, vel=v, acc=a)

            angle_rad = angle/180 * pi 
            t.orient.rotate_zt(angle_rad)
            rob.set_pose(t, vel=v, acc=a)

            print("Right UR: the current pose is : %s"  % rob.getl())
            printer.okg("Right UR: ************** Right UR Moved Successfully! ***************")            
            # time.sleep(0.0001)

            # forward pos[0] +
            # backward pos[0] -
            # up pos[1] -
            # down pos[1] +
            # left pos[2] +
            # right pos[2] -
            # move out 
            # rob.set_pose(t0, vel=v, acc=a)

        finally:
            pass
            # rob.close()
            # print("The UR3 robot is disconnected")


if __name__ == "__main__":
    rightrob = UR3.connectRightUR()
    try:
        if rightrob.is_program_running():
            pass
        else:
            printer.okg("Right UR starts to run!")
            # lh_displace = [3.06105, -1.69905, -3.02684]
            rh_displace = [-60, 0, 0]
            # left - right +
            final_angle = -60.0
            right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]
            UR3.moveRightPose(rightrob, right_pos_displace, final_angle)

            rh_displace = [-30, 0, 0]
            final_angle = 120.0
            right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]
            UR3.moveRightPose(rightrob, right_pos_displace, final_angle)

            rh_displace = [30, 0, 0]
            final_angle = -120.0
            right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]
            UR3.moveRightPose(rightrob, right_pos_displace, final_angle)

            time.sleep(6)

            time.sleep(6)

            rh_displace = [-175, -80, -40]
            final_angle = -65.0
            right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]
            UR3.moveRightPose(rightrob, right_pos_displace, final_angle)

            intial_joints = [0.10511700809001923, -2.754655663167135, -1.0462172667132776, 0.6226247549057007, -4.769015494977133, -0.06416160265077764] 
            rightrob.movej(intial_joints, acc= 0.25, vel=0.15)

            # rh_displace = [-30, 0, 0]
            # final_angle = -120.0
            # right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]
            # UR3.moveRightPose(rightrob, right_pos_displace, final_angle)

            # final_angle = 120.0
            # UR3.moveRightPose(rightrob, right_pos_displace, final_angle)
            # time.sleep(5)

            # right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]
            # final_angle = -120.0
            # UR3.moveRightPose(rightrob, right_pos_displace, final_angle)

        

            

    finally:
        rightrob.close()