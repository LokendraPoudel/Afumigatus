from unittest import TestCase
from edu.uchc.interactable.Cells import *

class TestTAFC(TestCase):
    def test_interact(self):
        a = Afumigatus(100)
        m = Macrophage()
        tf = Transferrin(100, 100)
        iron = Iron(100)

        tafc1 = TAFC(100, 100)
        tafc2 = TAFC(150, 150)

        print("TAFC X TAFC")
        print((tafc1.getTafc(), tafc2.getTafc(), tafc1.getTafcbi(), tafc2.getTafcbi()))
        tafc1.interact(tafc2)
        print((tafc1.getTafc(), tafc2.getTafc(), tafc1.getTafcbi(), tafc2.getTafcbi()))

        print("A.fumitatus X TAFC")
        print((a.iron_pool, tafc1.getTafc(), tafc1.getTafcbi()))
        a.interact(tafc1)
        print((a.iron_pool, tafc1.getTafc(), tafc1.getTafcbi()))

        print("macrophage X TAFC")
        print((m.iron_pool, tafc1.getTafc(), tafc1.getTafcbi()))
        m.interact(tafc1)
        print((m.iron_pool, tafc1.getTafc(), tafc1.getTafcbi()))

        print("TfBI X TAFC")
        print((tafc1.getTafc(), tafc1.getTafcbi(), tf.getTf(), tf.getTfBI()))
        tf.interact(tafc1)
        print((tafc1.getTafc(), tafc1.getTafcbi(), tf.getTf(), tf.getTfBI()))

        print("IRON X TAFC")
        print((tafc1.getTafc(), tafc1.getTafcbi(), iron.get()))
        iron.interact(tafc1)
        print((tafc1.getTafc(), tafc1.getTafcbi(), iron.get()))
