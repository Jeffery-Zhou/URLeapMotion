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

# data collection / paper

class UR3:
    # Left_UR3_IP = "158.132.172.193" 
    Right_UR3_IP = "158.132.172.214"

    @classmethod
    def connectLeftUR(cls):
        rob = urx.Robot(cls.Left_UR3_IP)
        rob.set_tcp((0,0,0,0,0,0))
        rob.set_payload(1.5, (0,0,0))
        time.sleep(0.2)
        printer.header("==================== Left UR3 connected. ====================")
        # intial_joints = [-0.0482409636126917, -0.748549763356344, 1.3524250984191895, -3.763566795979635, -1.5582435766803187, 9.371355835591451] 
        intial_joints = [-0.027399841939107716, -0.9967621008502405, 1.7950401306152344, -3.9452269713031214, -1.5623214880572718, 9.370444122944967]
        rob.movej(intial_joints, acc= 0.3, vel=0.2)
        printer.header("==================== Left UR3 finished initial setting. ====================")
        return rob

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
        rob.movej(intial_joints, acc= 0.3, vel=0.2)
        printer.header("==================== Right UR3 finished initial setting. ====================")
        return rob


    @classmethod 
    def moveLeftPose(cls, rob, pos_displace, angle = 0.0):
        try:
            l = 0.02
            v = 0.1    # velocity
            a = 0.2     # acceleration
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
            pass
            # rob.close()
            # print("The UR3 robot is disconnected")

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

class printer:   
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

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

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    logger = logging.getLogger(__name__)
    # leftrob = UR3.connectLeftUR() 
    rightrob = UR3.connectRightUR()


    def on_init(self, controller):
        printer.header("======================== LeapMotion Initialized ========================")
        # leftrob = UR3.connectLeftUR()

    def on_connect(self, controller):
        printer.okg("======================== Connected ========================")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        printer.warn("======================== Leap Motion Disconnected ========================")
        self.rightrob.close()
        printer.header("The UR3 right robot is disconnected")


    def on_exit(self, controller):
        printer.warn("========================  Leap Motion Listerner Exited ========================")
        self.rightrob.close()
        printer.header("The UR3 right robot is disconnected. ")


    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        cur_frame = controller.frame() # the current frame
        pre_frame = controller.frame(59) # the previous frame 1~59

        # A unique ID assigned to this Hand object, 
        # whose value remains the same across consecutive frames while the tracked hand remains visible. 
        # If tracking is lost (for example, when a hand is occluded by another hand or 
        # when it is withdrawn from or reaches the edge of the Leap Motion Controller field of view), 
        # the Leap Motion software may assign a new ID when it detects the hand in a future frame.


        if cur_frame.id % 20 == 0:
            fps = cur_frame.current_frames_per_second
            # print("Current FPS: %d " % int(fps))
            # print("Current Frame  id: %d, hands: %d, gestures: %d" % (cur_frame.id, len(cur_frame.hands), len(cur_frame.gestures())))
            # print("Previous Frame id: %d, hands: %d, gestures: %d" % (pre_frame.id, len(pre_frame.hands), len(pre_frame.gestures())))

            # two hands start otherwise do nothing
            if len(cur_frame.hands) == 1 and len(pre_frame.hands) == 1:
                if not cur_frame.hands[0].is_left:
                    right_hand_c = cur_frame.hands[0]
                else:
                    pass

                if not pre_frame.hands[0].is_left:
                    right_hand_p = pre_frame.hands[0]
                else:
                    pass

                print('') # separate the log
                print("Current FPS: %d " % int(fps))
                printer.header(" ========================= Current Frame  id: %d, hands: %d ========================= " % (cur_frame.id, len(cur_frame.hands)))
                print("Current   Right Hand %s, %s, %s" % (right_hand_c.palm_position, right_hand_c.direction, right_hand_c.palm_normal))
                print("Previous  Right Hand %s, %s, %s" % (right_hand_p.palm_position, right_hand_p.direction, right_hand_p.palm_normal))

                right_c_norm = right_hand_c.palm_normal
                right_p_norm = right_hand_p.palm_normal
                
                rh_displace = right_hand_c.palm_position - right_hand_p.palm_position        
                printer.warn("LeapMotion: the right hand displacement is %s" % rh_displace)
                right_pos_displace = [rh_displace[2]/500.0, -rh_displace[1]/500.0, rh_displace[0]/500.0]

                # angle_in_radians = Leap.Vector.x_axis.angle_to(Leap.Vector.y_axis)

                if right_c_norm[1] > 0:
                    printer.fail("Leap Motion: Please put your hand palm toward ground and hide UR3 job !")
                else:
                    # print(str(abs(left_c_norm[1]/left_c_norm[0])))
                    angle_c = math.acos( right_c_norm[1]*right_c_norm[1]/(right_c_norm[0] * right_c_norm[0] + right_c_norm[1] * right_c_norm[1]))
                    final_angle_c = right_c_norm[0]/abs(right_c_norm[0])*angle_c/pi * 180
                    printer.okg("Leap Motion: the hand palm normal is %s " % final_angle_c)

                    angle_p = math.acos( right_p_norm[1]*right_p_norm[1]/(right_p_norm[0] * right_p_norm[0] + right_p_norm[1] * right_p_norm[1]))
                    final_angle_p = right_p_norm[0]/abs(right_p_norm[0])*angle_p/pi * 180
                    printer.okg("Leap Motion: the hand palm normal is %s " % final_angle_p)
                    final_angle = final_angle_c - final_angle_p

                    if self.rightrob.is_program_running():
                        pass
                    else:
                        # UR3.moveLeftPose(self.rightrob, right_pos_displace, final_angle)
                        printer.okg("Left UR starts to run!")
                

                # ============ start of UR3 executor ================
                """ 
                # for real time performance
                threads = []
                threads.append(threading.Thread(target=UR3.moveLeftPose(self.leftrob, left_pos_displace)))
                threads.append(threading.Thread(target=UR3.moveRightPose(self.rightrob, right_pos_displace)))

                # Check the robot is runing
                if self.leftrob.is_program_running():
                    pass
                else:
                    threads[0].start()
                    printer.okb("Left UR thread starts to run!")

                if self.rightrob.is_program_running():
                    pass
                else:
                    threads[1].start()
                    printer.okb("Right UR thread starts to run!")
                
                """  
                # =========== end of UR3 excutor ================
            else:
                pass
            # two hands end
                

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"
 
        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
# End of SampleListener for LeapMotion

def runLeapMotion():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

def main():
    runLeapMotion()
    # leftrob = UR3.connectLeftUR()
    # UR3.movePose(leftrob)
    pass



if __name__ == "__main__":
    main()
