from unittest import TestCase
from edu.uchc.interactable.Cells import *

class TestAfumigatus(TestCase):
    def test_elongate(self):
        print("TEST ELONGATION")
        a1 = Afumigatus(None, None, None, status=Afumigatus.HYPHAE)
        a1.boolean_network[Afumigatus.LIP] = 1
        a2 = a1.elongate()
        print(a1)
        print(a2)
        print()

    def test_branch(self):
        print("TEST BRANCH")
        a1 = Afumigatus(None, None, None, status=Afumigatus.HYPHAE)
        for i in range(10):
            a1.branchable = True
            a1.boolean_network[Afumigatus.LIP] = 1
            a2 = a1.branch()
            print(a1)
            print(a2)
            print()
        print()

    def test_processBooleanNetwork(self):
        print("TEST PROCESS_BOOLEAN_NETWORK")
        #def __init__(self, iron, tafc, tafcbi, ironPool=0, status=0, isRoot=True):
        iron   = Molecule(100)
        tafc   = Molecule(100)
        tafcbi = Molecule(100)
        a = Afumigatus(iron, tafc, tafcbi)
        a.has_iron = True
        a.has_tafcbi = True

        print(a.boolean_network)
        print((iron.get(), tafc.get(), tafcbi.get()))
        a.process_boolean_network()
        print(a.boolean_network)
        print((iron.get(), tafc.get(), tafcbi.get()))
        print()

    def test_secreteTAFC(self):
        print("TEST SECRET_TAFC")
        iron = Molecule(100)
        tafc = Molecule(100)
        tafcbi = Molecule(100)
        a = Afumigatus(iron, tafc, tafcbi)
        a.boolean_network[Afumigatus.TAFC] = 1

        print(tafc.get())
        a.secrete_tafc()
        print(tafc.get())
        print()

    def test_updateStatus(self):
        print("TEST UPDATE_STATUS")
        a = Afumigatus(None, None, None)
        while(a.status != Afumigatus.HYPHAE):
            a.update_status()
            print(a.status)
        print()

    def test_diffuseIron(self):
        print("TEST DIFFUSE_IRON")
        a = Afumigatus(None, None, None, 1024, status=Afumigatus.HYPHAE)
        a0 = a
        list = []
        for i in range(10):
            a0.boolean_network[Afumigatus.LIP] = 1
            a1 = a0.elongate()
            a2 = a0.branch()
            print((a0, a1, a2))
            #print((a0.ironPool, a1.ironPool, a2.ironPool))
            a0 = a1
            list.append(a0)
        print(a.iron_pool)
        for i in range(400): a.diffuse_iron()
        print(a.iron_pool)
        for a in list:
            print(a.iron_pool)


    def test_interact(self):
        print("TEST INTERACT")
        m = Macrophage(None, None, None)
        tf = Transferrin(None, 100)
        iron = Iron(100)
        tfbi = TransferrinBI(100)
        af = Afumigatus(None, None, None, status = Afumigatus.SWELLING_CONIDIA)

        print((tf.get(), tfbi.get(), iron.get()))
        print(tf.interact(af))
        print((tf.get(), tfbi.get(), iron.get(), af.has_iron))
        print(tfbi.interact(af))
        print((tf.get(), tfbi.get(), iron.get(), af.has_iron))
        print(iron.interact(af))
        print((tf.get(), tfbi.get(), iron.get(), af.has_iron))

        while(not m.attached_fungus):
            print(m.interact(af))
            print(m.attached_fungus)


