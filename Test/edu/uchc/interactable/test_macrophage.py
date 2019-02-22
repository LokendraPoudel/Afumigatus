from unittest import TestCase
from edu.uchc.interactable.Cells import Macrophage
from edu.uchc.interactable.Molecules import *

class TestMacrophage(TestCase):
    def test_interact(self):
        m1 = Macrophage(None, None, None)
        m2 = Macrophage(None, None, None)
        print(m1.interact(m2))
        print()


    def test_processBooleanNetwork(self):
        iron = Molecule(10)
        tfbi = Molecule(10)
        tf = Molecule(10)
        m = Macrophage(iron, tfbi, tf)
        m.has_iron = True
        m.has_tfbi = True
        print(m.boolean_network)
        print(m.iron_pool)
        m.process_boolean_network()
        print(m.boolean_network)
        print(m.iron_pool)
        print()


    def test_secreteIron(self):
        iron = Molecule(10)
        tfbi = Molecule(10)
        tf = Molecule(10)
        m = Macrophage(iron, tfbi, tf)
        m.iron_pool = 10
        m.boolean_network[Macrophage.Fpn] = 1
        print(str(tfbi.get()) + " " + str(m.iron_pool))
        m.secrete_iron()
        print(str(tfbi.get()) + " " + str(m.iron_pool))
        print()


    def test_updateStatus(self):
        m = Macrophage(None, None, None)
        m.status = Macrophage.INFECTED
        for i in range(Constants.ITER_TO_CHANGE_STATE):
            m.update_status()
            print(m.status)
        m.update_status()
        print(m.status)
        print()
