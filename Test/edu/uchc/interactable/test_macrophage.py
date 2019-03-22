from unittest import TestCase
from edu.uchc.interactable.Cells import Macrophage
from edu.uchc.interactable.Molecules import *

class TestMacrophage(TestCase):
    def test_interact(self):
        m1 = Macrophage()
        m2 = Macrophage()
        print(m1.interact(m2))
        print()


    def test_processBooleanNetwork(self):
        m = Macrophage()
        m.has_iron = True
        m.has_tfbi = True
        print(m.boolean_network)
        m.process_boolean_network()
        print(m.boolean_network)
        print()


    def test_secreteIron(self):
        tf = Transferrin(10, 0)
        m = Macrophage(50)
        m.boolean_network[Macrophage.Fpn] = 1
        print(str(tf.getTf()) + " " +str(tf.getTfBI()) + " " + str(m.iron_pool))
        m.secrete(tf)
        print(str(tf.getTf()) + " " +str(tf.getTfBI()) + " " + str(m.iron_pool))
        print()


    def test_updateStatus(self):
        m = Macrophage()
        m.status = Macrophage.INFECTED
        for i in range(Constants.ITER_TO_CHANGE_STATE):
            m.update_status()
            print(m.status)
        m.update_status()
        print(m.status)
        print()
