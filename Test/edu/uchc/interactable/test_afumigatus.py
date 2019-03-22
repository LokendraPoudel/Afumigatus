from unittest import TestCase
from edu.uchc.interactable.Cells import *
#from edu.uchc.interactable.Molecules import *

class TestAfumigatus(TestCase):
    def test_elongate(self):
        print("TEST ELONGATION")
        a1 = Afumigatus(status=Afumigatus.HYPHAE)
        a1.boolean_network[Afumigatus.LIP] = 1
        a2 = a1.elongate()
        print(a1)
        print(a2)
        print()

    def test_branch(self):
        print("TEST BRANCH")
        a1 = Afumigatus(status=Afumigatus.HYPHAE)
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
        a = Afumigatus()
        a.boolean_network[Afumigatus.Fe] = 1
        a.boolean_network[Afumigatus.TAFCBI] = 1

        print(a.boolean_network)
        a.process_boolean_network()
        print(a.boolean_network)
        print()

    def test_secreteTAFC(self):
        print("TEST SECRET_TAFC")
        tafc = TAFC(0, 0)
        a = Afumigatus()
        a.boolean_network[Afumigatus.TAFC] = 1

        print(tafc.getTafc())
        a.secrete(tafc)
        print(tafc.getTafc())
        print()

    def test_updateStatus(self):
        print("TEST UPDATE_STATUS")
        a = Afumigatus()
        while(a.status != Afumigatus.HYPHAE):
            a.update_status()
            print(a.status)
        print()

    def test_diffuseIron(self):
        print("TEST DIFFUSE_IRON")
        a = Afumigatus(1024, status=Afumigatus.HYPHAE)
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
        m = Macrophage()
        tf = Transferrin(100, 100)
        iron = Iron(100)
        af = Afumigatus(status = Afumigatus.SWELLING_CONIDIA)

        print((tf.getTf(), tf.getTfBI(), iron.get()))
        print(tf.interact(af))
        print((tf.getTf(), tf.getTfBI(), iron.get(), af.boolean_network[Afumigatus.Fe]))
        print(iron.interact(af))
        print((tf.getTf(), tf.getTfBI(), iron.get(), af.boolean_network[Afumigatus.Fe]))

        while(m.boolean_network[Macrophage.Bglucan] != 1):
            print(m.interact(af))
            print(m.attached_fungus)


