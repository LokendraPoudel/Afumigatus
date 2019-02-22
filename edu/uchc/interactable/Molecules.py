from edu.uchc.interactable.Util import Constants
from edu.uchc.interactable.Util import Util

class Molecule():

    def __init__(self, moelcule):
        self._molecule = moelcule;

    def inc(self, qtty):
        self._molecule = self._molecule + qtty
        return self._molecule

    def dec(self, qtty):
        self._molecule = self._molecule - qtty
        return self._molecule

    def pdec(self, p):
        self._molecule = self._molecule - self._molecule*p
        return self._molecule

    def pinc(self, p):
        self._molecule = self._molecule + self._molecule * p
        return self._molecule

    def set(self, qtty):
        self._molecule = qtty

    def get(self):
        return self._molecule

class Iron(Molecule):

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is Iron:
            return None
        elif type(interactable) is Macrophage:
            interactable.has_iron = interactable._selected(self._molecule)
            return None
        return interactable.interact(self)

class TransferrinBI(Molecule):

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is TransferrinBI:
            return None
        elif type(interactable) is Macrophage:
            interactable.has_tfbi = interactable._selected(self._molecule)
            return None
        elif type(interactable) is Transferrin:
            return None
        elif type(interactable) is Iron:
            return None
        return interactable.interact(self)


class Transferrin(Molecule):

    def __init__(self, tfbi, qtty):
        super().__init__(qtty)
        self.tfbi = tfbi

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is Transferrin:
            return None
        elif type(interactable) is Macrophage:
            return None
        elif type(interactable) is Iron:
            iron = interactable.get()
            v = Util.michaelianKinetics(iron, self._molecule, Constants.KM)
            interactable.dec(v)
            self._molecule = self._molecule - v
            self.tfbi.inc(v)
            return self.tfbi
        return interactable.interact(self)

class TAFC(Molecule):

    def __init__(self, tafcbi, tf, qtty):
        super().__init__(qtty)
        self.tafcbi = tafcbi
        self.tf = tf

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage, Afumigatus

        if type(interactable) is TAFC:
            return None
        elif type(interactable) is Macrophage:
            return None
        elif type(interactable) is TransferrinBI:
            tfbi = interactable.get()
            v = Util.michaelianKinetics(tfbi, self._molecule, Constants.KM)
            interactable.dec(v)
            self.tf.inc(v)
            self.tafcbi.inc(v);
            self._molecule = self._molecule - v
            return self.tafcbi
        elif type(interactable) is Transferrin:
            return None
        elif type(interactable) is Afumigatus:
            return None
        elif type(interactable) is Iron:
            iron = interactable.get()
            v = Util.michaelianKinetics(iron, self._molecule, Constants.KM)
            interactable.dec(v)
            self._molecule = self._molecule - v
            self.tafcbi.inc(v)
            return self.tafcbi
        return interactable.interact(self)


class TAFCBI(Molecule):

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage, Afumigatus
        if type(interactable) is TAFCBI:
            return None
        elif type(interactable) is Macrophage:
            return None
        elif type(interactable) is Iron:
            return None
        elif type(interactable) is TAFC:
            return None
        elif type(interactable) is TransferrinBI:
            return None
        elif type(interactable) is Transferrin:
            return None
        elif type(interactable) is Afumigatus:
            interactable.has_tafcbi = True
            return None
        return interactable.interact(self)



