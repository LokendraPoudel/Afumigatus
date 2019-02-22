from unittest import TestCase
from edu.uchc.interactable.Molecules import *
from edu.uchc.interactable.Cells import Macrophage

class TestTransferrinBI(TestCase):
    def test_interact(self):
        m = Macrophage(None, None, None)
        tf = Transferrin(None, 100)
        iron = Iron(100)

        tfbi = TransferrinBI(100)
        print((tf.get(), iron.get(), tfbi.get()))
        print(tf.interact(tfbi))
        print((tf.get(), iron.get(), tfbi.get()))
        print(iron.interact(tfbi))
        print((tf.get(), iron.get(), tfbi.get()))
        m.interact(tfbi)
        print(m.has_tfbi)
