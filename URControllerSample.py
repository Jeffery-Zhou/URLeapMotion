import urx
import logging
import time
from math import pi
# "158.132.172.193"
Left_Hand_IP_ADDRESS = "158.132.172.193"
Right_Hand_IP_ADDRESS = "158.132.172.214"

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot(Right_Hand_IP_ADDRESS)
    # rob.set_tcp((0,0,0,0,0,0))
    # rob.set_payload(1.5, (0,0,0))
    time.sleep(0.2)
    try:
        l = 0.05
        v = 0.1
        a = 0.2

        j = rob.getj() # the join variable
        print("The initial joint space is %s \n" % str(j))
        """
        [0.5243943950121863, -0.07798659231070386, 0.25202923769305685, -0.06403291554008664, -3.094951547164568, 0.017947641504043658]
        intial_joints = [-0.027399841939107716, -0.9967621008502405, 1.7950401306152344, -3.9452269713031214, -1.5623214880572718, 9.370444122944967]
        [-0.04778606096376592, -0.5796015898333948, 1.056783676147461, -2.9077709356891077, -1.480461899434225, 7.9925705830203455]
        """
        

        # left joints [-0.03303844133485967, -0.4258616606341761, 1.2580962181091309, -3.8896873633014124, -1.6458943525897425, 9.371907297764913] 
        # right joints [0.10511700809001923, -2.754655663167135, -1.0462172667132776, 0.6226247549057007, -4.769015494977133, -0.06416160265077764] 

        # intial_joints = [0.039932187646627426, -2.416210476552145, -1.6089499632464808, 0.8271387815475464, -4.680840078984396, -0.06411344209779912] 
        # [0.039932187646627426, -2.416210476552145, -1.6089499632464808, 0.8271387815475464, -4.680840078984396, -0.06411344209779912] 
        # left [-0.0482409636126917, -0.748549763356344, 1.3524250984191895, -3.763566795979635, -1.5582435766803187, 9.371355835591451] 
        # intial_joints = [-0.027399841939107716, -0.9967621008502405, 1.7950401306152344, -3.9452269713031214, -1.5623214880572718, 9.370444122944967] 
        # rob.movej(intial_joints, acc= 0.2, vel=0.1)

        # pose = rob.getl() # TCP pose in base coordinate
        # print(str(pose))

        
        """
        # [-0.5769171757373774, -0.10113988817781773, 0.14814405962135802, 
        # 2.7339925137441417, -0.20349272032382887, -1.249864646487075]
        """    

        # t = rob.get_pose() # the transformation from base to TCP (Base T_ tool)
        # print(str(t))
        # t.orient.rotate_zt(pi/18)
        # rob.set_pose(t, vel=v, acc=a)


        """ 
        <Transform:
        <Orientation: 
                    array([
                        [ 0.64818186, -0.06887272, -0.75836457],
                        [-0.17524891, -0.98266078, -0.06054429],
                        [-0.74104528,  0.17214627, -0.64901276]
                        ])>
        <Vector: (-0.57692, -0.10114, 0.14814)>
        >
        """


        # time.sleep(2)

        # pose[1] += l
        # rob.movel(pose, acc=a, vel=v) # abosultely move

        # rob.translate((0, 0, -l), acc=a, vel=v) # translate tool in base coordinate
        # rob.translate_tool((0, 0, -l), acc=a, vel=v) # translate tool in tool coordnate

        # print("Current position of the tcp is %s \n" % str(t.pos))
        # print(str(t.pos[0]))
        # print(str(t.orient))






        # # get current pose, transform it and move robot to new pose
        # trans = rosbot.get_pose()  # get current transformation matrix (tool to base)
        # trans.pos.z += 0.3
        # trans.orient.rotate_yb(pi/2)
        # robot.set_pose(trans, acc=0.5, vel=0.2)  # apply the new pose


        # #or only work with orientation part
        # o = robot.get_orientation()
        # o.rotate_yb(pi)
        # robot.set_orientation(o)


        # rotate_t: perceived in the transformed reference system.

    finally:
        rob.close()
        print("The UR3 robot is disconnected")

