from unittest import TestCase
from edu.uchc.interactable.Cells import *


class TestTAFCBI(TestCase):
    def test_interact(self):
        a = Afumigatus(None, None, None, 100)
        m = Macrophage(None, None, None)
        tfbi = TransferrinBI(100)
        tf = Transferrin(None, 100)
        iron = Iron(100)
        tafc = TAFC(None, tf, 100)

        tafcbi1 = TAFCBI(100)
        tafcbi2 = TAFCBI(150)


        print("TAFCBI X TAFCBI")
        print((tafcbi1.get(), tafcbi2.get()))
        tafcbi1.interact(tafcbi2)
        print((tafcbi1.get(), tafcbi2.get()))

        print("TAFC X TAFCBI")
        print((tafcbi1.get(), tafc.get()))
        tafc.interact(tafcbi1)
        print((tafcbi1.get(), tafc.get()))

        print("macrophage X TAFCBI")
        print((m.iron_pool, tafcbi1.get()))
        m.interact(tafcbi1)
        print((m.iron_pool, tafcbi1.get()))

        print("TfBI X TAFCBI")
        print((tafcbi1.get(), tfbi.get()))
        tfbi.interact(tafcbi1)
        print((tafcbi1.get(), tfbi.get()))

        print("Tf X TAFCBI")
        print((tafcbi1.get(), tf.get()))
        tf.interact(tafcbi1)
        print((tafcbi1.get(), tf.get()))

        print("IRON X TAFCBI")
        print((tafcbi1.get(), iron.get()))
        iron.interact(tafcbi1)
        print((tafcbi1.get(), iron.get()))

        print("A.fumitatus X TAFCBI")
        print((a.has_tafcbi, tafcbi1.get()))
        a.interact(tafcbi1)
        print((a.has_tafcbi, tafcbi1.get()))
