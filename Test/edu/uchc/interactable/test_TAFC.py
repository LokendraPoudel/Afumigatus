from unittest import TestCase
from edu.uchc.interactable.Cells import *

class TestTAFC(TestCase):
    def test_interact(self):
        a = Afumigatus(None, None, None, 100)
        m = Macrophage(None, None, None)
        tfbi = TransferrinBI(100)
        tf = Transferrin(None, 100)
        iron = Iron(100)

        tafcbi = Molecule(100)
        tafc1 = TAFC(tafcbi, tf, 100)
        tafc2 = TAFC(tafcbi, tf, 150)

        print("TAFC X TAFC")
        print((tafc1.get(), tafc2.get()))
        tafc1.interact(tafc2)
        print((tafc1.get(), tafc2.get()))

        print("A.fumitatus X TAFC")
        print((a.iron_pool, tafc1.get()))
        a.interact(tafc1)
        print((a.iron_pool, tafc1.get()))

        print("macrophage X TAFC")
        print((m.iron_pool, tafc1.get()))
        m.interact(tafc1)
        print((m.iron_pool, tafc1.get()))

        print("TfBI X TAFC")
        print((tafc1.get(), tfbi.get()))
        tafcbi = tfbi.interact(tafc1)
        print((tafc1.get(), tfbi.get(), tafcbi.get()))

        print("Tf X TAFC")
        print((tafc1.get(), tf.get()))
        tf.interact(tafc1)
        print((tafc1.get(), tf.get()))

        print("IRON X TAFC")
        print((tafc1.get(), iron.get()))
        iron.interact(tafc1)
        print((tafc1.get(), iron.get()))