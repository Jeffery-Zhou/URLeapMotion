import urx
from IPython import embed
import logging

Left_Hand_IP_ADDRESS = "158.132.172.193"


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        #robot = urx.Robot("192.168.1.6")
        robot = urx.Robot(Left_Hand_IP_ADDRESS)
        #robot = urx.Robot("localhost")
        r = robot
        print("Robot object is available as robot or r")
        embed()
    finally:
        robot.close()
