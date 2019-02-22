from edu.uchc.interactable.Util import Constants
from random import random
from edu.uchc.interactable.Molecules import *
from edu.uchc.interactable.Util import Util

class Macrophage():
    FREE = 0
    INFECTED = 1

    Dectin1 = 0
    TNFa = 1
    IL6 = 2
    Ft = 3
    DMT1 = 4
    LIP = 5
    TFR = 6
    Fe2 = 7
    IRP = 8
    Hep = 9
    Fpn = 10
    TFBI = 11
    Bglucan = 12

    SPECIES_NUM = 13

    def __init__(self, iron, tfbi, transferrin):
        self.iron = iron
        self.tfbi = tfbi
        self.transferrin = transferrin
        self.boolean_network = Constants.InitMacrophageBooleanState;

        self.has_iron = False
        self.has_tfbi = False
        self.attached_fungus = False
        self.iron_pool = 0;
        self.iteration = 0
        self.status = Macrophage.FREE

    def interact(self, interactable):
        if(type(interactable) is Macrophage):
            return(None)
        return(interactable.interact(self))

    def process_boolean_network(self):
        temp = [0 for _ in range(Macrophage.SPECIES_NUM)]

        temp[Macrophage.Dectin1] = self.boolean_network[Macrophage.Bglucan]
        temp[Macrophage.TNFa] = self.boolean_network[Macrophage.Dectin1]
        temp[Macrophage.IL6] = self.boolean_network[Macrophage.Dectin1]
        temp[Macrophage.Ft] = self.boolean_network[Macrophage.TNFa] | (-self.boolean_network[Macrophage.IRP] + 1)
        temp[Macrophage.DMT1] = self.boolean_network[Macrophage.TNFa]
        temp[Macrophage.LIP] = ((-self.boolean_network[Macrophage.Ft] + 1) | \
                                (self.boolean_network[Macrophage.DMT1] & self.boolean_network[Macrophage.Fe2]) | \
                                (self.boolean_network[Macrophage.TFBI] & self.boolean_network[Macrophage.TFR]) | (-self.boolean_network[Macrophage.Fpn] + 1))
        temp[Macrophage.TFR] = self.boolean_network[Macrophage.IRP]
        temp[Macrophage.Fe2] = 1 if self.has_iron else 0 #self.hasIron ? 1: 0
        temp[Macrophage.IRP] = -self.boolean_network[Macrophage.LIP] + 1
        temp[Macrophage.Hep] = self.boolean_network[Macrophage.IL6]
        temp[Macrophage.Fpn] = (-self.boolean_network[Macrophage.IRP] + 1) | (-self.boolean_network[Macrophage.Hep] + 1)
        temp[Macrophage.TFBI] = 1 if self.has_tfbi else 0 #self.hasTfbi ? 1: 0
        temp[Macrophage.Bglucan] = 1 if self.attached_fungus else 0 #self.attachedFungus ? 1: 0

        for i in range(Macrophage.SPECIES_NUM):
            self.boolean_network[i] = temp[i]

        self.attached_fungus = False

        if self.boolean_network[Macrophage.TFBI] == 1 and self.boolean_network[Macrophage.TFR] == 1:
            qtty = Constants.BASE_QTTY * self._activation(self.tfbi.get());
            self.tfbi.dec(qtty);
            self.transferrin.inc(qtty);
            self.iron_pool = self.iron_pool + qtty;


        if self.boolean_network[Macrophage.Fe2] == 1 and self.boolean_network[Macrophage.DMT1] == 1:
            qtty = Constants.BASE_QTTY * self._activation(self.iron.get());
            self.iron.dec(qtty);
            self.iron_pool = self.iron_pool + qtty;

    def secrete_iron(self):
        if (self.boolean_network[Macrophage.Fpn] == 1):
            iron_qtty = self.iron_pool;
            tf_qtty = Constants.BASE_QTTY * self._activation(self.transferrin.get());
            v = Util.michaelianKinetics(iron_qtty, tf_qtty, Constants.KM);

            self.iron_pool -= v;
            self.transferrin.dec(v);
            self.tfbi.inc(v);


        return self.iron;

    def update_status(self):
        if (self.status == Macrophage.INFECTED):
            self.iteration = self.iteration + 1
            if (self.iteration >= Constants.ITER_TO_CHANGE_STATE):
                self.iteration = 0;
                self.status = Macrophage.FREE;

    def _activation(self, level):
        return(level * level / (level * level + Constants.KM * Constants.KM))

    def _selected(self, level):
        return random() < level*level/(level*level + Constants.KM*Constants.KM)


class Afumigatus():
    RESTING_CONIDIA = 0
    SWELLING_CONIDIA = 1
    GERMINATING = 2
    HYPHAE = 3
    DEAD = 4

    hapX = 0
    sreA = 1
    HapX = 2
    SreA = 3
    RIA = 4
    EstB = 5
    MirB = 6
    SidA = 7
    TAFC = 8
    ICP = 9
    LIP = 10
    CccA = 11
    FC0fe = 12
    FC1fe = 13
    VAC = 14
    ROS = 15
    Yap1 = 16
    SOD2_3 = 17
    Cat1_2 = 18
    ThP = 19
    Fe = 20
    O = 21
    TAFCBI = 22
    SPECIES_NUM = 23


    def __init__(self, iron, tafc, tafcbi, ironPool = 0, status = 0, isRoot = True):
        self.iron = iron
        self.tafc = tafc
        self.tafcbi = tafcbi

        self.iron_pool = ironPool
        self.status = status
        self.is_root = isRoot

        self.growable = True
        self.branchable = False
        self.iteration = 0
        self.boolean_network = Constants.InitAfumigatusBooleanState

        self.next_septa = None
        self.next_branch = None

        self.has_iron = False
        self.has_tafcbi = False

    def elongate(self):
        if self.growable and self.status == Afumigatus.HYPHAE and self.boolean_network[Afumigatus.LIP] == 1:
            self.growable = False;
            self.branchable = True;
            self.iron_pool = self.iron_pool / 2.0;
            self.next_septa = Afumigatus(self.iron, self.tafc, self.tafcbi, self.iron_pool, Afumigatus.HYPHAE, False);
            return self.next_septa;
        return self

    def branch(self):
        if self.branchable and self.status == Afumigatus.HYPHAE and self.boolean_network[Afumigatus.LIP] == 1:
            if random() < Constants.P_BRANCH:
                self.iron_pool = self.iron_pool / 2.0;
                self.next_branch = Afumigatus(self.iron, self.tafc, self.tafcbi, self.iron_pool, Afumigatus.HYPHAE, False);
                return self.next_branch;
            self.branchable = False;
        return self

    def interact(self, interactable):
        from edu.uchc.interactable.Molecules import TransferrinBI, Transferrin, Iron
        if type(interactable) is Afumigatus:
            return None
        elif type(interactable) is Iron:
            self.has_iron = self._selected(interactable.get());
            return None
        elif type(interactable) is TransferrinBI:
            return None
        elif type(interactable) is Transferrin:
            return None
        elif type(interactable) is Macrophage:
            if interactable.status == Macrophage.FREE and random() < Constants.MACROPHAGE_AFUMIGAUTS_ITER_PROB:
                if not (self.status == Afumigatus.RESTING_CONIDIA or self.status == Afumigatus.DEAD):
                    interactable.attached_fungus = True
                if self.status == Afumigatus.SWELLING_CONIDIA or self.status == Afumigatus.RESTING_CONIDIA:
                    self.status = Afumigatus.DEAD
                    interactable.status = Macrophage.INFECTED
                    interactable.iron_pool = interactable.iron_pool + self.iron_pool
            return None
        return interactable.interact(self)

    def process_boolean_network(self):
        temp = [0 for i in range(Afumigatus.SPECIES_NUM)]

        temp[Afumigatus.hapX] = -self.boolean_network[Afumigatus.SreA] + 1
        temp[Afumigatus.sreA] = -self.boolean_network[Afumigatus.HapX] + 1
        temp[Afumigatus.HapX] = self.boolean_network[Afumigatus.hapX] & (-self.boolean_network[Afumigatus.LIP] + 1)
        temp[Afumigatus.SreA] = self.boolean_network[Afumigatus.sreA] & self.boolean_network[Afumigatus.LIP]
        temp[Afumigatus.RIA] = -self.boolean_network[Afumigatus.SreA] + 1
        temp[Afumigatus.EstB] = -self.boolean_network[Afumigatus.SreA] + 1
        temp[Afumigatus.MirB] = self.boolean_network[Afumigatus.HapX] & (-self.boolean_network[Afumigatus.SreA] + 1)
        temp[Afumigatus.SidA] = self.boolean_network[Afumigatus.HapX] & (-self.boolean_network[Afumigatus.SreA] + 1)
        temp[Afumigatus.TAFC] = self.boolean_network[Afumigatus.SidA]
        temp[Afumigatus.ICP] = (-self.boolean_network[Afumigatus.HapX] + 1) & (self.boolean_network[Afumigatus.VAC] | self.boolean_network[Afumigatus.FC1fe])
        temp[Afumigatus.LIP] = ((self.boolean_network[Afumigatus.TAFCBI] & self.boolean_network[Afumigatus.MirB] & self.boolean_network[Afumigatus.EstB]) | \
                                (self.boolean_network[Afumigatus.Fe] & self.boolean_network[Afumigatus.RIA]))
        temp[Afumigatus.CccA] = -self.boolean_network[Afumigatus.HapX] + 1
        temp[Afumigatus.FC0fe] = self.boolean_network[Afumigatus.SidA]
        temp[Afumigatus.FC1fe] = self.boolean_network[Afumigatus.LIP] & self.boolean_network[Afumigatus.FC0fe]
        temp[Afumigatus.VAC] = self.boolean_network[Afumigatus.LIP] & self.boolean_network[Afumigatus.CccA]
        temp[Afumigatus.ROS] = self.boolean_network[Afumigatus.LIP] | \
                               (self.boolean_network[Afumigatus.O] & (- (self.boolean_network[Afumigatus.SOD2_3] & self.boolean_network[Afumigatus.ThP] \
                                                                         & self.boolean_network[Afumigatus.Cat1_2]) + 1)) \
                               | (self.boolean_network[Afumigatus.ROS] & (- (self.boolean_network[Afumigatus.SOD2_3] \
                                                                             & (self.boolean_network[Afumigatus.ThP] | self.boolean_network[Afumigatus.Cat1_2])) + 1))
        temp[Afumigatus.Yap1] = self.boolean_network[Afumigatus.ROS]
        temp[Afumigatus.SOD2_3] = self.boolean_network[Afumigatus.Yap1]
        temp[Afumigatus.Cat1_2] = self.boolean_network[Afumigatus.Yap1] & (-self.boolean_network[Afumigatus.HapX] + 1)
        temp[Afumigatus.ThP] = self.boolean_network[Afumigatus.Yap1];

        temp[Afumigatus.Fe] = 1 if self.has_iron else 0 # might change according to iron environment?
        temp[Afumigatus.O] = self.boolean_network[Afumigatus.O];
        temp[Afumigatus.TAFCBI] = 1 if self.has_tafcbi else 0

        for i in range(Afumigatus.SPECIES_NUM):
            self.boolean_network[i] = temp[i]

        if self.boolean_network[Afumigatus.Fe] == 1 and self.boolean_network[Afumigatus.RIA] == 1:
            qtty = Constants.BASE_QTTY * self._activation(self.iron.get())
            self.iron.dec(qtty)
            self.iron_pool = self.iron_pool + qtty

        if self.boolean_network[Afumigatus.TAFCBI] == 1 and self.boolean_network[Afumigatus.MirB] == 1 and self.boolean_network[Afumigatus.EstB] == 1:
            qtty = Constants.BASE_QTTY * self._activation(self.tafcbi.get())
            self.tafcbi.dec(qtty)
            self.iron_pool = self.iron_pool + qtty


    def secrete_tafc(self):
        if self.boolean_network[Afumigatus.TAFC] == 1:
            self.tafc.inc(Constants.BASE_QTTY)
        return self.tafc

    def update_status(self):
        self.iteration = self.iteration + 1
        if self.status == Afumigatus.RESTING_CONIDIA and self.iteration > Constants.ITER_TO_CHANGE_STATE:
            self.status = Afumigatus.SWELLING_CONIDIA
            self.iteration = 0
        elif self.status == Afumigatus.SWELLING_CONIDIA and self.iteration > Constants.ITER_TO_CHANGE_STATE:
            self.status = Afumigatus.GERMINATING
            self.iteration = 0
        elif self.status == Afumigatus.GERMINATING and self.iteration > Constants.ITER_TO_CHANGE_STATE:
            self.status = Afumigatus.HYPHAE

    def diffuse_iron(self, afumigatus = None):
        if afumigatus == None:
            if self.is_root:
                self.diffuse_iron(self)
        else:
            if afumigatus.next_septa != None and afumigatus.next_branch == None:
                current_iron_pool = afumigatus.iron_pool
                next_iron_pool = afumigatus.next_septa.iron_pool
                iron_pool = (current_iron_pool + next_iron_pool) / 2.0
                afumigatus.iron_pool = iron_pool
                afumigatus.next_septa.iron_pool = iron_pool
                self.diffuse_iron(afumigatus.next_septa)
            elif afumigatus.next_septa != None and afumigatus.next_branch != None:
                current_iron_pool = afumigatus.iron_pool
                next_iron_pool = afumigatus.next_septa.iron_pool
                branch_iron_pool = afumigatus.next_branch.iron_pool
                iron_pool = (current_iron_pool + next_iron_pool + branch_iron_pool) / 3.0
                afumigatus.iron__pool = iron_pool
                afumigatus.next_septa.iron_pool = iron_pool
                afumigatus.next_branch.iron_pool = iron_pool
                self.diffuse_iron(afumigatus.next_branch)
                self.diffuse_iron(afumigatus.next_septa)

    def _selected(self, level):
        return random() < level * level / (level * level + Constants.KM * Constants.KM)

    def _activation(self, level):
        return level * level / (level * level + Constants.KM * Constants.KM)
