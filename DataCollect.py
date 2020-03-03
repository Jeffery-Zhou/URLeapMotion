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
    def moveLeftPose(cls, rob, pos_displace, angle = 0.0):
        try:
            l = 0.02
            v = 0.10    # velocity
            a = 0.20     # acceleration
            pose = rob.getl()
            t = rob.get_pose()
            # t0 = rob.get_pose()
            print("Left UR: the current pose is : %s"  % t.pos)
            # print("Translate in -x and rotate")
            # t0.orient.rotate_zb(pi/18)
            for i in range(3):
                if i == 0: # in / out
                    t.pos[i] += pos_displace[i]/3.0
                elif i == 1: # up / down
                    t.pos[i] += pos_displace[i]/1.5
                else:   # left / right
                    t.pos[i] += pos_displace[i]/2.0
            print("Left UR: the target pose is %s with a displacement %s" % (t.pos, pos_displace))
            # pose=list(t.pos)
            # rob.movel(pose, vel=v, acc=a)

            angle_rad = angle/180 * pi 
            t.orient.rotate_zt(angle_rad)
            rob.set_pose(t, vel=v, acc=a)

            print("Left UR: the changed pose is : %s"  % rob.getl())
            printer.okg("Left UR: ************** Left UR Moved Successfully! ***************")
            # time.sleep(0.005)
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

    @classmethod 
    def moveRightPose(cls, rob, pos_displace):
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
                    pose[i] += pos_displace[i]/3.0
                elif i == 1: # up / down
                    pose[i] += pos_displace[i]/1.5
                else:   # left / right
                    pose[i] += pos_displace[i]/2.0
            print("Right UR: the target pose is %s with a displacement %s" % (pose, pos_displace))
            rob.movel(pose, vel=v, acc=a)
            print("Right UR: the current pose is : %s"  % rob.getl())
            printer.okg("Right UR: ************** Right UR Moved Successfully! ***************")
            
            time.sleep(0.0001)

            # forward pos[0] +
            # backward pos[0] -
            # up pos[1] -
            # down pos[1] +
            # left pos[2] +
            # right pos[2] -
            # move out 
            # rob.set_pose(t0, vel=v, acc=a)

        finally:
            rob.close()
            # print("The UR3 robot is disconnected")


if __name__ == "__main__":
    leftrob = UR3.connectLeftUR()
    try:
        if leftrob.is_program_running():
            pass
        else:
            printer.okg("Left UR starts to run!")
            # lh_displace = [3.06105, -1.69905, -3.02684]

            #----------------------------
            lh_displace = [60, 0, 0]
            # left - right +
            final_angle = 60.0
            left_pos_displace = [-lh_displace[2]/500.0, -lh_displace[1]/500.0, -lh_displace[0]/500.0]
            UR3.moveLeftPose(leftrob, left_pos_displace, final_angle)
            #----------------------------
            time.sleep(6)
            #----------------------------
            time.sleep(6)   
            #----------------------------
            lh_displace = [30, 0, 0]
            left_pos_displace = [-lh_displace[2]/500.0, -lh_displace[1]/500.0, -lh_displace[0]/500.0]
            final_angle = -120.0
            UR3.moveLeftPose(leftrob, left_pos_displace, final_angle)
            #----------------------------
            lh_displace = [-30, 0, 0]
            left_pos_displace = [-lh_displace[2]/500.0, -lh_displace[1]/500.0, -lh_displace[0]/500.0]
            final_angle = 120.0
            UR3.moveLeftPose(leftrob, left_pos_displace, final_angle)

            #----------------------------
            lh_displace = [180, -80, -240]

            left_pos_displace = [-lh_displace[2]/500.0, -lh_displace[1]/500.0, -lh_displace[0]/500.0]
            final_angle = 70.0
            UR3.moveLeftPose(leftrob, left_pos_displace, final_angle)

            #----------------------------
            intial_joints = [-0.03303844133485967, -0.4258616606341761, 1.2580962181091309, -3.8896873633014124, -1.6458943525897425, 9.371907297764913] 
            leftrob.movej(intial_joints, acc= 0.3, vel=0.2)

            # UR3.moveLeftPose(leftrob, left_pos_displace, final_angle)

            # time.sleep(3)

    finally:
        leftrob.close()