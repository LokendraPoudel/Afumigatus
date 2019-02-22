from unittest import TestCase
from edu.uchc.interactable.Cells import Macrophage
from edu.uchc.interactable.Molecules import *

class TestIron(TestCase):
    def test_interact(self):
        m = Macrophage(None, None, None)
        iron1 = Iron(100)
        iron2 = Iron(150)
        print(iron1.interact(iron2))
        print((iron1.get(), iron2.get()))
        print(m.has_iron)
        print(m.interact(iron1))
        print((iron1.get(), m.has_iron))
