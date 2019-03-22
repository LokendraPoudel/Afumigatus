from unittest import TestCase
from edu.uchc.interactable.Molecules import *
from edu.uchc.interactable.Cells import Macrophage

class TestTransferrin(TestCase):
    def test_interact(self):
        m = Macrophage(50)
        iron = Iron(10)
        tf = Transferrin(10, 10)
        print((iron.get(), tf.getTf(), tf.getTfBI()))
        print(iron.interact(tf))
        print((iron.get(), tf.getTf(), tf.getTfBI()))
        print(m.interact(tf))
        print((iron.get(), tf.getTf(), tf.getTfBI()))
