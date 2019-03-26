from unittest import TestCase
from edu.uchc.interactable.Cells import *

class TestROS(TestCase):
    def test_interact(self):
        a = Afumigatus(100)
        m = Macrophage()
        tf = Transferrin(100, 100)
        iron = Iron(100)
        tafc = TAFC(100, 100)

        ros1 = ROS(100)
        ros2 = ROS(100)



        print("ROS X ROS")
        print((ros2.get()))
        ros2.interact(ros2)
        print((ros2.get()))

        print("A.fumitatus X ROS")
        print((a.boolean_network[Afumigatus.ROS], ros1.get()))
        a.interact(ros1)
        print((a.boolean_network[Afumigatus.ROS], ros1.get()))

        print("macrophage X ROS")
        print((ros1.get()))
        m.interact(ros1)
        print((ros1.get()))

        print("TfBI X ros")
        print((ros1.get(), tf.getTf(), tf.getTfBI()))
        tf.interact(ros1)
        print((ros1.get(), tf.getTf(), tf.getTfBI()))

        print("ROS X TAFC")
        print((tafc.getTafc(), tafc.getTafcbi(), ros1.get()))
        ros1.interact(tafc)
        print((tafc.getTafc(), tafc.getTafcbi(), ros1.get()))

        print("ROS X IRON")
        print((iron.get(), ros1.get()))
        ros1.interact(iron)
        print((iron.get(), ros1.get()))
