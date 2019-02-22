from unittest import TestCase
from edu.uchc.interactable.Molecules import *
from edu.uchc.interactable.Cells import Macrophage

class TestTransferrin(TestCase):
    def test_interact(self):
        m = Macrophage(None, None, None)
        tfbi = Molecule(0)
        iron = Iron(10)
        tf = Transferrin(tfbi, 10)
        print((iron.get(), tf.get(), tf.tfbi.get()))
        print(iron.interact(tf))
        print((iron.get(), tf.get(), tf.tfbi.get()))
        print(m.interact(tf))
