
import urx
import logging
import time
from math import pi
# "158.132.172.193"
Left_Hand_IP_ADDRESS = "158.132.172.193"

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot(Left_Hand_IP_ADDRESS)
    # rob.set_tcp((0,0,0,0,0,0))
    # rob.set_payload(1.5, (0,0,0))
    time.sleep(0.2)
    try:
        l = 0.05
        v = 0.01
        a = 0.1
        pose = rob.getl() # TCP pose in base coordinate

        t = rob.get_pose() # from base to TCP
        # the pose of toll center point()
        # [-0.3014919897420241, 0.39872794273334866, 0.15162112980739711, -0.2292156668555865, -1.5254596121610757, -0.2638322212085911]

        print("the before pose is %s" % pose)
        displacement = [3.08298, 0, 0]
        for i in range(3):
            pose[i] += displacement[i]

        print("the after  pose is %s with a displacement %s" % (pose, displacement))
        rob.movel(pose, acc=a, vel=v) # abosultely move

        print("the current pose is %s " % rob.get_pose())

        # time.sleep(0.2)
        # print("absolute move in base coordinate ")
        # pose[2] += l
        # # pose 0:x, 1:y, 2:z, 3:pitch, 4:roll, 5:yaw
        # rob.movel(pose, acc=a, vel=v)
        # # absolutely move in base coordinate

        # time.sleep(0.2)
        rob.translate((0, 0, -l), acc=a, vel=v) 
        # move tool in base coordinate, keeping orientation

        # time.sleep(0.2)
        rob.translate_tool((0, 0, -l), acc=a, vel=v)
        # move tool in tool coordinate, keeping orientation

        # time.sleep(0.2)
        j = rob.getj()
        # get joints position
        

        # print("Translate in -x and rotate")
        # # set_to_x_rotation
        t.orient.rotate_zt(pi/18)
        t.pos[0] -= l
        rob.set_pose(t, vel=v, acc=a)
        # set a pose by transformation


        # get current pose, transform it and move robot to new pose
        trans = robot.get_pose()  # get current transformation matrix (tool to base)
        trans.pos.z += 0.3
        trans.orient.rotate_yb(pi/2)
        robot.set_pose(trans, acc=0.5, vel=0.2)  # apply the new pose


        #or only work with orientation part
        o = robot.get_orientation()
        o.rotate_yb(pi)
        robot.set_orientation(o)

        # set_to_x_rotation: Replace this orientation by that of a rotation around x.
        # set_to_y_rotation: Replace this orientation by that of a rotation around y.
        # set_to_z_rotation: Replace this orientation by that of a rotation around z. 

        # rotate_t: perceived in the transformed reference system.

    finally:
        rob.close()
        print("The UR3 robot is disconnected")

