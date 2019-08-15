from edu.uchc.interactable.Util import Constants
from edu.uchc.interactable.Util import Util
from random import random
from abc import ABC, abstractmethod

class Molecule(ABC):

    @abstractmethod
    def __init__(self, qtty):
        pass

    @abstractmethod
    def inc(self, qtty, index=0):
        pass

    @abstractmethod
    def dec(self, qtty, index=0):
        pass

    @abstractmethod
    def pdec(self, p, index=0):
        pass

    @abstractmethod
    def pinc(self, p, index=0):
        pass

    @abstractmethod
    def set(self, qtty, index=0):
        pass

    @abstractmethod
    def get(self, index=0):
        pass


class Iron(Molecule):

    total_iron = 0;
    NUM_STATES = 1

    def __init__(self, qtty):
        self._iron = qtty
        Iron.total_iron = Iron.total_iron + qtty

    def inc(self, qtty, index=0):
        self._iron = self._iron + qtty
        Iron.total_iron = Iron.total_iron + qtty
        return self._iron

    def dec(self, qtty, index=0):
        self._iron = self._iron - qtty
        Iron.total_iron = Iron.total_iron - qtty
        return self._iron

    def pdec(self, p, index=0):
        self._iron = self._iron - self._iron*p
        Iron.total_iron = Iron.total_iron - self._iron*p
        return self._iron

    def pinc(self, p, index=0):
        self._iron = self._iron + self._iron * p
        Iron.total_iron = Iron.total_iron + self._iron * p
        return self._iron

    def set(self, qtty, index=0):
        Iron.total_iron = Iron.total_iron - self._iron
        Iron.total_iron = Iron.total_iron + qtty
        self._iron = qtty

    def get(self, index=0):
        return self._iron

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is Iron:
            return False
        elif type(interactable) is Macrophage:
            if interactable.boolean_network[Macrophage.DMT1] == 1 and Util.hillProbability(self.get()) > random():
                qtty = Constants.UPTAKE_QTTY * self.get();
                interactable.boolean_network[Macrophage.Fe2] = 1
                self.dec(qtty);
                interactable.inc_iron_pool(qtty)
            return True
        return interactable.interact(self)


class Transferrin(Molecule):

    total_transferrin = [0, 0]
    #total_transferrinBI = 0

    INDEXES = {"Tf": 0, "TfBI": 1}
    NUM_STATES = 2

    def __init__(self, tf, tfbi):
        self._tf = [tf, tfbi]
        Transferrin.total_transferrin[0] = Transferrin.total_transferrin[0] + tf
        Transferrin.total_transferrin[1] = Transferrin.total_transferrin[1] + tfbi

    def inc(self, qtty, index=0):
        if type(index) is str:
            index = Transferrin.INDEXES[index]
        self._tf[index] = self._tf[index] + qtty
        Transferrin.total_transferrin[index] = Transferrin.total_transferrin[index] + qtty
        return self._tf[index]

    def dec(self, qtty, index=0):
        if type(index) is str:
            index = Transferrin.INDEXES[index]
        self._tf[index] = self._tf[index] - qtty
        Transferrin.total_transferrin[index] = Transferrin.total_transferrin[index] - qtty
        return self._tf[index]

    def pdec(self, p, index=0):
        if type(index) is str:
            index = Transferrin.INDEXES[index]
        dec =  self._tf[index] * p
        self._tf[index] = self._tf[index] - dec
        Transferrin.total_transferrin[index] = Transferrin.total_transferrin[index] - dec
        return self._tf[index]

    def pinc(self, p, index=0):
        if type(index) is str:
            index = Transferrin.INDEXES[index]
        inc = self._tf[index] * p
        self._tf[index] = self._tf[index] + inc
        Transferrin.total_transferrin[index] = Transferrin.total_transferrin[index] + inc
        return self._tf[index]

    def set(self, qtty, index=0):
        if type(index) is str:
            index = Transferrin.INDEXES[index]
        Transferrin.total_transferrin[index] = Transferrin.total_transferrin[index] - self._tf[index]
        Transferrin.total_transferrin[index] = Transferrin.total_transferrin[index] + qtty
        self._tf[index] = qtty

    def get(self, index=0):
        if type(index) is str:
            index = Transferrin.INDEXES[index]
        return self._tf[index]

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage
        if type(interactable) is Transferrin:
            return False
        elif type(interactable) is Macrophage:
            #interactable.boolean_network[Macrophage.TFBI] = interactable.selected(self.get("TfBI"))
            #if interactable.boolean_network[Macrophage.TFBI] == 1 and interactable.boolean_network[Macrophage.TFR] == 1:
            if Util.hillProbability(self.get("TfBI")) < random():
                interactable.boolean_network[Macrophage.TFBI] = 1
                qtty = self.get("TfBI") * Constants.MPH_UPTAKE_QTTY
                self.dec(qtty, "TfBI")
                self.inc(qtty, "Tf");
                interactable.inc_iron_pool(qtty)
            #if (interactable.boolean_network[Macrophage.Fpn] == 1):
            #    v = Constants.IRON_QTTY * interactable.iron_pool;

            #   interactable.inc_iron_pool(-v)
            #   self.dec(v, "Tf");
            #   self.inc(v, "TfBI");
            return True
        elif type(interactable) is Iron:
            iron = interactable.get()
            v = Util.michaelianKinetics(iron, self.get("Tf"))
            interactable.dec(v)
            self.dec(v, "Tf")
            self.inc(v, "TfBI")

            return v!=0
        return interactable.interact(self)

class TAFC(Molecule):

    total_tafc = [0, 0]
    #total_tafcbi = 0
    INDEXES = {"TAFC": 0, "TAFCBI": 1}
    NUM_STATES = 2

    def __init__(self, tafc, tafcbi):
        self._tafc = [tafc, tafcbi]
        TAFC.total_tafc[0] = TAFC.total_tafc[0] + tafc
        TAFC.total_tafc[1] = TAFC.total_tafc[1] + tafcbi

        #self.Lac = Lac
        #self.Tf = Tf

    def inc(self, qtty, index=0):
        if type(index) is str:
            index = TAFC.INDEXES[index]
        self._tafc[index] = self._tafc[index] + qtty
        TAFC.total_tafc[index] = TAFC.total_tafc[index] + qtty
        return self._tafc[index]

    def dec(self, qtty, index=0):
        if type(index) is str:
            index = TAFC.INDEXES[index]
        self._tafc[index] = self._tafc[index] - qtty
        TAFC.total_tafc[index] = TAFC.total_tafc[index] - qtty
        return self._tafc

    def pdec(self, p, index=0):
        if type(index) is str:
            index = TAFC.INDEXES[index]
        dec = self._tafc[index] * p
        self._tafc[index] = self._tafc[index] - dec
        TAFC.total_tafc[index] = TAFC.total_tafc[index] - dec
        return self._tafc[index]

    def pinc(self, p, index=0):
        if type(index) is str:
            index = TAFC.INDEXES[index]
        inc = self._tafc[index] * p
        self._tafc[index] = self._tafc[index] + inc
        TAFC.total_tafc[index] = TAFC.total_tafc[index] + inc
        return self._tafc

    def set(self, qtty, index=0):
        if type(index) is str:
            index = TAFC.INDEXES[index]
        TAFC.total_tafc[index] = TAFC.total_tafc[index] - self._tafc[index]
        TAFC.total_tafc[index] = TAFC.total_tafc[index] + qtty
        self._tafc[index] = qtty

    def get(self, index=0):
        if type(index) is str:
            index = TAFC.INDEXES[index]
        return self._tafc[index]

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage, Afumigatus
        from random import random

        if type(interactable) is TAFC:
            return False
        elif type(interactable) is Macrophage:
            return False
        elif type(interactable) is Transferrin:
            v = Util.michaelianKinetics(interactable.get("TfBI"), self.get("TAFC"))
            #if not self._tafc[0] == 0:
            #    print((self._tafc[0], self._tafc[1], interactable.get("TfBI"), v))
            interactable.dec(v, "TfBI")
            interactable.inc(v, "Tf")
            self.inc(v, "TAFCBI")
            self.dec(v, "TAFC")

            return v != 0
        elif type(interactable) is Afumigatus:
            if interactable.boolean_network[Afumigatus.MirB] == 1 and interactable.boolean_network[Afumigatus.EstB] == 1 and \
                    Util.hillProbability(self.get("TAFCBI")) > random():
                interactable.boolean_network[Afumigatus.TAFCBI] = 1
                qtty = self.get("TAFCBI") * Constants.AF_UPTAKE_QTTY
                self.dec(qtty, "TAFCBI")
                interactable.inc_iron_pool(qtty)
            if interactable.boolean_network[Afumigatus.TAFC] == 1 and interactable.status != Afumigatus.RESTING_CONIDIA: # SECRETE TAFC
                self.inc(Constants.TAFC_QTTY, "TAFC")
            return True
        elif type(interactable) is Iron:
            v = Util.michaelianKinetics(interactable.get(), self.get("TAFC"))
            interactable.dec(v)
            self.dec(v, "TAFC")
            self.inc(v, "TAFCBI")

            return v != 0

        return interactable.interact(self)

class ROS(Molecule):

    total_ros = 0
    NUM_STATES = 1

    def __init__(self, qtty):
        self._ros = qtty
        ROS.total_ros = ROS.total_ros + qtty

    def inc(self, qtty, index=0):
        self._ros = self._ros + qtty
        ROS.total_ros = ROS.total_ros + qtty
        return self._ros

    def dec(self, qtty, index=0):
        self._ros = self._ros - qtty
        ROS.total_ros = ROS.total_ros - qtty
        return self._ros

    def pdec(self, p, index=0):
        self._ros = self._ros - self._ros * p
        ROS.total_ros = ROS.total_ros - self._ros * p
        return self._ros

    def pinc(self, p, index=0):
        self._ros = self._ros + self._ros * p
        ROS.total_ros = ROS.total_ros + self._ros * p
        return self._ros

    def set(self, qtty, index=0):
        ROS.total_ros = ROS.total_ros - self._ros
        ROS.total_ros = ROS.total_ros + qtty
        self._ros = qtty

    def get(self, index=0):
        return self._ros

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Afumigatus, Macrophage

        if type(interactable) is ROS:
            self.dec(self.get())
            return False
        elif type(interactable) is Transferrin:
            return False
        elif type(interactable) is TAFC:
            return False
        elif type(interactable) is Iron:
            return False
        elif type(interactable) is Afumigatus:
            interactable.boolean_network[Afumigatus.O] = (1 if Util.hillProbability(self.get()) > random() else 0)
            return True
        elif type(interactable) is Macrophage:
            #if interactable.boolean_network[Macrophage.LIP] == 1 and interactable.status == Macrophage.INFECTED:
            #    self.inc(Constants.ROS_QTTY)
            return True
        return interactable.interact(self)

class Lactoferrin(Molecule):

    total_lactoferrin = [0, 0]
    INDEXES = {"Lactoferrin": 0, "LactoferrinBI": 1}
    NUM_STATES = 2

    def __init__(self, lactoferrin, lactoferrinbi):
        self._lactoferrin = [lactoferrin, lactoferrinbi]
        Lactoferrin.total_lactoferrin[0] = Lactoferrin.total_lactoferrin[0] + lactoferrin
        Lactoferrin.total_lactoferrin[1] = Lactoferrin.total_lactoferrin[1] + lactoferrinbi

    def inc(self, qtty, index=0):
        if type(index) is str:
            index = Lactoferrin.INDEXES[index]
        self._lactoferrin[index] = self._lactoferrin[index] + qtty
        Lactoferrin.total_lactoferrin[index] = Lactoferrin.total_lactoferrin[index] + qtty
        return self._lactoferrin[index]

    def dec(self, qtty, index=0):
        if type(index) is str:
            index = Lactoferrin.INDEXES[index]
        self._lactoferrin[index] = self._lactoferrin[index] - qtty
        Lactoferrin.total_lactoferrin[index] = Lactoferrin.total_lactoferrin[index] - qtty
        return self._lactoferrin

    def pdec(self, p, index=0):
        if type(index) is str:
            index = Lactoferrin.INDEXES[index]
        dec = self._lactoferrin[index] * p
        self._lactoferrin[index] = self._lactoferrin[index] - dec
        Lactoferrin.total_lactoferrin[index] = Lactoferrin.total_lactoferrin[index] - dec
        return self._lactoferrin[index]

    def pinc(self, p, index=0):
        if type(index) is str:
            index = Lactoferrin.INDEXES[index]
        inc = self._lactoferrin[index] * p
        self._lactoferrin[index] = self._lactoferrin[index] + inc
        Lactoferrin.total_lactoferrin[index] = Lactoferrin.total_lactoferrin[index] + inc
        return self._lactoferrin

    def set(self, qtty, index=0):
        if type(index) is str:
            index = Lactoferrin.INDEXES[index]
        Lactoferrin.total_lactoferrin[index] = Lactoferrin.total_lactoferrin[index] - self._lactoferrin[index]
        Lactoferrin.total_lactoferrin[index] = Lactoferrin.total_lactoferrin[index] + qtty
        self._lactoferrin[index] = qtty

    def get(self, index=0):
        if type(index) is str:
            index = Lactoferrin.INDEXES[index]
        return self._lactoferrin[index]

    def interact(self, interactable):
        from edu.uchc.interactable.Cells import Macrophage, Afumigatus, Neutrophil
        if type(interactable) is Lactoferrin:
            return False
        if type(interactable) is Macrophage:
            return False
        if type(interactable) is Afumigatus:
            return False
        if type(interactable) is Neutrophil:
            if Util.hillProbability(self.get("LactoferrinBI")) > random(): #interactable.selected(self.get("LactoferrinBI")) == 1:
                qtty = self.get("LactoferrinBI") * Constants.MPH_UPTAKE_QTTY
                self.dec(qtty, "LactoferrinBI")
                interactable.inc_iron_pool(qtty)
            if interactable.status == Neutrophil.INTERACTING:
                self.inc(Constants.LAC_QTTY, "Lactoferrin")
            return True
        if type(interactable) is TAFC:
            return False
        if type(interactable) is Transferrin:
            v = Util.michaelianKinetics(interactable.get("TfBI"), self.get("Lactoferrin"))
            interactable.dec(v, "TfBI")
            interactable.inc(v, "Tf")
            self.inc(v, "LactoferrinBI")
            self.dec(v, "Lactoferrin")
            return v!=0
        if type(interactable) is Iron:
            v = Util.michaelianKinetics(interactable.get(), self.get("Lactoferrin"))
            interactable.dec(v)
            self.dec(v, "Lactoferrin")
            self.inc(v, "LactoferrinBI")
            return v!=0
        if type(interactable) is ROS:
            return False
        return interactable.interact(self)