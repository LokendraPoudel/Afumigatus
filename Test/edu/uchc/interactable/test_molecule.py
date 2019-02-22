from unittest import TestCase
from edu.uchc.interactable.Molecules import Molecule

class TestIron(TestCase):
    def test(self):
        molecule = Molecule(10)
        molecule.pdec(0.5)
        print(molecule.get())
        molecule.dec(4)
        print(molecule.get())
        molecule.inc(10)
        print(molecule.get())