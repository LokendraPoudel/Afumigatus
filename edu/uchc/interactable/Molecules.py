from edu.uchc.interactable.Util import Constants
from edu.uchc.interactable.Util import Util

class Iron:

    total_iron = 0;

    def __init__(self, qtty):
        self._iron = qtty
        Iron.total_iron = Iron.total_iron + qtty

    def inc(self, qtty):
        self._iron = self._iron + qtty
        Iron.total_iron = Iron.total_iron + qtty
        return self._iron

    def dec(self, qtty):
        self._iron = self._iron - qtty
        Iron.total_iron = Iron.total_iron - qtty
        return self._iron

    def pdec(self, p):
        self._iron = self._iron - self._iron*p
        Iron.total_iron = Iron.total_iron - self._iron*p
        return self._iron

    def pinc(self, p):
        self._iron = self._iron + self._iron * p
        Iron.total_iron = Iron.total_iron + self._iron * p
        return self._iron

    def get(self):
        return self._iron

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is Iron:
            return False
        elif type(interactable) is Macrophage:
            interactable.boolean_network[Macrophage.Fe2] = interactable.selected(self._iron)
            if interactable.boolean_network[Macrophage.Fe2] == 1 and interactable.boolean_network[Macrophage.DMT1] == 1:
                qtty = Constants.BASE_QTTY * interactable.activation(self.get());
                self.dec(qtty);
                interactable.inc_iron_pool(qtty)
            return True
        return interactable.interact(self)


class Transferrin:

    total_transferrin = 0
    total_transferrinBI = 0

    def __init__(self, tf, tfbi):
        self._tf = tf
        self._tfbi = tfbi
        Transferrin.total_transferrin = Transferrin.total_transferrin + tf
        Transferrin.total_transferrinBI = Transferrin.total_transferrinBI + tfbi

    def incTf(self, qtty):
        self._tf = self._tf + qtty
        Transferrin.total_transferrin = Transferrin.total_transferrin + qtty
        return self._tf

    def decTf(self, qtty):
        self._tf = self._tf - qtty
        Transferrin.total_transferrin = Transferrin.total_transferrin - qtty
        return self._tf

    def pdecTf(self, p):
        self._tf = self._tf - self._tf * p
        Transferrin.total_transferrin = Transferrin.total_transferrin - self._tf * p
        return self._tf

    def pincTf(self, p):
        self._tf = self._tf + self._tf * p
        Transferrin.total_transferrin = Transferrin.total_transferrin + self._tf * p
        return self._tf

    def getTf(self):
        return self._tf

    def incTfBI(self, qtty):
        self._tfbi = self._tfbi + qtty
        Transferrin.total_transferrinBI = Transferrin.total_transferrinBI + qtty
        return self._tfbi

    def decTfBI(self, qtty):
        self._tfbi = self._tfbi - qtty
        Transferrin.total_transferrinBI = Transferrin.total_transferrinBI - qtty
        return self._tfbi

    def pdecTfBI(self, p):
        self._tfbi = self._tfbi - self._tf * p
        Transferrin.total_transferrinBI = Transferrin.total_transferrinBI - self._tf * p
        return self._tfbi

    def pincTfBI(self, p):
        self._tfbi = self._tfbi + self._tfbi * p
        Transferrin.total_transferrinBI = Transferrin.total_transferrinBI + self._tf * p
        return self._tfbi

    def getTfBI(self):
        return self._tfbi

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is Transferrin:
            return False
        elif type(interactable) is Macrophage:
            interactable.boolean_network[Macrophage.TFBI] = interactable.selected(self.getTfBI())
            if interactable.boolean_network[Macrophage.TFBI] == 1 and interactable.boolean_network[Macrophage.TFR] == 1:
                qtty = Constants.BASE_QTTY * interactable.activation(self.getTfBI());
                self.decTfBI(qtty)
                self.incTf(qtty);
                interactable.inc_iron_pool(qtty)
            if (interactable.boolean_network[Macrophage.Fpn] == 1):
                iron_qtty = interactable.iron_pool;
                tf_qtty = Constants.BASE_QTTY * interactable.activation(self.getTf());
                v = Util.michaelianKinetics(iron_qtty, tf_qtty, Constants.KM);

                interactable.inc_iron_pool(-v)
                self.decTf(v);
                self.incTfBI(v);
            return True
        elif type(interactable) is Iron:
            iron = interactable.get()
            v = Util.michaelianKinetics(iron, self.getTf(), Constants.KM)
            interactable.dec(v)
            self.decTf(v)
            self.incTfBI(v)

            return True
        return interactable.interact(self)

class TAFC:

    total_tafc = 0
    total_tafcbi = 0

    def __init__(self, tafc, tafcbi):
        self._tafc = tafc
        self._tafcbi = tafcbi
        TAFC.total_tafc = TAFC.total_tafc + tafc
        TAFC.total_tafcbi = TAFC.total_tafcbi + tafcbi

    def incTafc(self, qtty):
        self._tafc = self._tafc + qtty
        TAFC.total_tafc = TAFC.total_tafc + qtty
        return self._tafc

    def decTafc(self, qtty):
        self._tafc = self._tafc - qtty
        TAFC.total_tafc = TAFC.total_tafc - qtty
        return self._tafc

    def pdecTafc(self, p):
        self._tafc = self._tafc - self._tafc * p
        TAFC.total_tafc = TAFC.total_tafc - self._tafc * p
        return self._tafc

    def pincTafc(self, p):
        self._tafc = self._tafc + self._tafc * p
        TAFC.total_tafc = TAFC.total_tafc + self._tafc * p
        return self._tafc

    def getTafc(self):
        return self._tafc

    def incTafcbi(self, qtty):
        self._tafcbi = self._tafcbi + qtty
        TAFC.total_tafcbi = TAFC.total_tafcbi + qtty
        return self._tafcbi

    def decTafcbi(self, qtty):
        self._tafcbi = self._tafcbi - qtty
        TAFC.total_tafcbi = TAFC.total_tafcbi - qtty
        return self._tafcbi

    def pdecTafcbi(self, p):
        self._tafcbi = self._tafcbi - self._tf * p
        TAFC.total_tafcbi = TAFC.total_tafcbi - self._tf * p
        return self._tafcbi

    def pincTafcbi(self, p):
        self._tafcbi = self._tafcbi + self._tfbi * p
        TAFC.total_tafcbi = TAFC.total_tafcbi + self._tf * p
        return self._tafcbi

    def getTafcbi(self):
        return self._tafcbi

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage, Afumigatus

        if type(interactable) is TAFC:
            return False
        elif type(interactable) is Macrophage:
            return False
        elif type(interactable) is Transferrin:
            v = Util.michaelianKinetics(interactable.getTfBI(), self.getTafc(), Constants.KM)
            interactable.decTfBI(v)
            interactable.incTf(v)
            self.incTafcbi(v)
            self.decTafc(v)

            return True
        elif type(interactable) is Afumigatus:
            interactable.boolean_network[Afumigatus.TAFCBI] = 1 # REVIEW
            if interactable.boolean_network[Afumigatus.TAFCBI] == 1 and interactable.boolean_network[Afumigatus.MirB] == 1 and interactable.boolean_network[Afumigatus.EstB] == 1:
                qtty = Constants.BASE_QTTY * interactable.activation(self.getTafcbi())
                self.decTafcbi(qtty)
                interactable.inc_iron_pool(qtty)
            if interactable.boolean_network[Afumigatus.TAFC] == 1: # SECRETE TAFC
                self.incTafc(Constants.BASE_QTTY)
            return True
        elif type(interactable) is Iron:
            v = Util.michaelianKinetics(interactable.get(), self.getTafc(), Constants.KM)
            interactable.dec(v)
            self.decTafc(v)
            self.incTafcbi(v)

            return True

        return interactable.interact(self)



