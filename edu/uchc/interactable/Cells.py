from edu.uchc.interactable.Util import Constants
from random import random
from random import randint
from edu.uchc.interactable.Molecules import *
from edu.uchc.interactable.Util import Util
from abc import ABC, abstractmethod
import numpy as np
import math

class Cell(ABC):

    @abstractmethod
    def process_boolean_network(self):
        pass

    @abstractmethod
    def update_status(self):
        pass

    @abstractmethod
    def is_dead(self):
        pass



class Macrophage(Cell):
    InitMacrophageBooleanState = [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1]

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

    total_iron = 0

    def __init__(self, iron_pool = 0):
        self.boolean_network = Macrophage.InitMacrophageBooleanState;
        self.iron_pool = iron_pool;
        self.iteration = 0
        self.afumigatus = None
        self.status = Macrophage.FREE
        Macrophage.total_iron = Macrophage.total_iron + iron_pool

    def interact(self, interactable):
        if(type(interactable) is Macrophage):
            return False
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
        temp[Macrophage.Fe2] = 0 #self.hasIron ? 1: 0
        temp[Macrophage.IRP] = -self.boolean_network[Macrophage.LIP] + 1
        temp[Macrophage.Hep] = self.boolean_network[Macrophage.IL6]
        temp[Macrophage.Fpn] = (-self.boolean_network[Macrophage.IRP] + 1) | (-self.boolean_network[Macrophage.Hep] + 1)
        temp[Macrophage.TFBI] = 0 #self.hasTfbi ? 1: 0
        temp[Macrophage.Bglucan] = 0 #self.attachedFungus ? 1: 0

        for i in range(Macrophage.SPECIES_NUM):
            self.boolean_network[i] = temp[i]


    def update_status(self):
        if self.status == Macrophage.INFECTED:
            self.iteration += 1
        if self.afumigatus == None and self.iteration == Constants.ITER_TO_LYMPHOCYTES_CHANGE_STATE:
            self.status = Macrophage.FREE
            self.iteration = 0
        elif self.afumigatus != None and self.boolean_network[Macrophage.LIP] == 1:
            self.afumigatus.status = Afumigatus.DEAD
            self.afumigatus = None
            self.iteration = 0

    def is_dead(self):
        return False

#    def activation(self, level, K=Constants.K):
#        return(level * level / (level * level + K * K))
#
#    def selected(self, level, K=Constants.K):
#        return 1 if random() < level*level/(level*level + K*K) else 0

    def inc_iron_pool(self, qtty):
        self.iron_pool = self.iron_pool + qtty
        Macrophage.total_iron = Macrophage.total_iron + qtty


class Afumigatus(Cell):
    InitAfumigatusBooleanState = [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    RESTING_CONIDIA = 0
    SWELLING_CONIDIA = 1
    HYPHAE = 2
    DEAD = 3
    INTERNALIZED = 4

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

    total_iron = 0
    total_afumigatus = 0


    def __init__(self, x=0, y=0, z=0, ironPool = 0, status = 0, isRoot = True):
        self.iron_pool = ironPool
        self.status = status
        self.is_root = isRoot
        self.x = x
        self.y = y
        self.z = z
        self.dx = 0.02*(random() - 1)
        self.dy = 0.02*(random() - 1)
        self.dz = 0.02*(random() - 1)

        self.growable = True
        self.branchable = False
        self.iteration = 0
        self.boolean_network = Afumigatus.InitAfumigatusBooleanState

        self.next_septa = None
        self.next_branch = None
        self.previous_septa = None
        self.Fe = False

        Afumigatus.total_iron = Afumigatus.total_iron + ironPool
        Afumigatus.total_afumigatus = Afumigatus.total_afumigatus + 1

    def elongate(self):
        #print((self.growable, self.status == Afumigatus.HYPHAE, self.boolean_network[Afumigatus.LIP]))
        if self.growable and self.status == Afumigatus.HYPHAE and self.boolean_network[Afumigatus.LIP] == 1:
            self.growable = False;
            self.branchable = True;
            self.iron_pool = self.iron_pool / 2.0;
            self.next_septa = Afumigatus(x=self.x + self.dx, y=self.y + self.dy, z=self.z + self.dz,ironPool=0, status=Afumigatus.HYPHAE, isRoot=False)
            self.next_septa.previous_septa = self
            self.next_septa.iron_pool = self.iron_pool
            return self.next_septa;
        return self

    def branch(self):
        if self.branchable and self.status == Afumigatus.HYPHAE and self.boolean_network[Afumigatus.LIP] == 1:
            if random() < Constants.P_BRANCH:
                self.iron_pool = self.iron_pool / 2.0
                growth_vector = [self.dx, self.dy, self.dz]
                B = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], growth_vector])
                B_inv = np.linalg.inv(B)
                R = Util.rotatation_matrix(2*random()*math.pi)
                R = np.dot(B, np.dot(R, B_inv))
                growth_vector = np.dot(R, growth_vector)

                self.next_branch = Afumigatus(x=self.x + growth_vector[0], y=self.y + growth_vector[1], z=self.z + growth_vector[2], ironPool=0, status=Afumigatus.HYPHAE, isRoot=False);
                self.next_branch.iron_pool = self.iron_pool
                self.next_branch.previous_septa = self
                return self.next_branch;
            self.branchable = False;
        return self

    def interact(self, interactable):
        from edu.uchc.interactable.Molecules import Transferrin, Iron
        if type(interactable) is Afumigatus:
            return False
        elif type(interactable) is Iron:
            if self.boolean_network[Afumigatus.RIA] == 1 and Util.hillProbability(interactable.get()) > random():
                qtty = interactable.get() * Constants.UPTAKE_QTTY
                self.boolean_network[Afumigatus.Fe] = 1
                interactable.dec(qtty)
                self.inc_iron_pool(qtty)
            return True
        elif type(interactable) is Transferrin:
            return False
        elif type(interactable) is Macrophage:
            if interactable.status == Macrophage.FREE:# and random() < Constants.MACROPHAGE_AFUMIGAUTS_ITER_PROB:
                if not self.status == Afumigatus.DEAD:
                    interactable.status = Macrophage.INFECTED
                if not (self.status == Afumigatus.RESTING_CONIDIA or self.status == Afumigatus.DEAD):
                    interactable.boolean_network[Macrophage.Bglucan] = 1
                #if self.status == Afumigatus.SWELLING_CONIDIA or self.status == Afumigatus.RESTING_CONIDIA:
                    #self.status = Afumigatus.INTERNALIZED
                    #interactable.afumigatus = self
                    #interactable.inc_iron_pool(self.iron_pool)
                    #self.inc_iron_pool(-self.iron_pool)
            return True
        return interactable.interact(self)

    def process_boolean_network(self):
        temp = [0 for i in range(Afumigatus.SPECIES_NUM)]

        self.has_iron()

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
                                (self.boolean_network[Afumigatus.Fe] & self.boolean_network[Afumigatus.RIA]) | (1 if self.Fe else 0))
        temp[Afumigatus.CccA] = -self.boolean_network[Afumigatus.HapX] + 1
        temp[Afumigatus.FC0fe] = self.boolean_network[Afumigatus.SidA]
        temp[Afumigatus.FC1fe] = self.boolean_network[Afumigatus.LIP] & self.boolean_network[Afumigatus.FC0fe]
        temp[Afumigatus.VAC] = self.boolean_network[Afumigatus.LIP] & self.boolean_network[Afumigatus.CccA]
        # temp[Afumigatus.ROS] = self.boolean_network[Afumigatus.LIP] | \
        #                        (self.boolean_network[Afumigatus.O] & (- (self.boolean_network[Afumigatus.SOD2_3] & self.boolean_network[Afumigatus.ThP] \
        #                         & self.boolean_network[Afumigatus.Cat1_2]) + 1)) \
        #                        | (self.boolean_network[Afumigatus.ROS] & (- (self.boolean_network[Afumigatus.SOD2_3] \
        #                         & (self.boolean_network[Afumigatus.ThP] | self.boolean_network[Afumigatus.Cat1_2])) + 1))
        temp[Afumigatus.ROS] = (self.boolean_network[Afumigatus.O] & (- (self.boolean_network[Afumigatus.SOD2_3] & self.boolean_network[Afumigatus.ThP] \
                               & self.boolean_network[Afumigatus.Cat1_2]) + 1)) \
                              | (self.boolean_network[Afumigatus.ROS] & (- (self.boolean_network[Afumigatus.SOD2_3] \
                               & (self.boolean_network[Afumigatus.ThP] | self.boolean_network[Afumigatus.Cat1_2])) + 1))
        temp[Afumigatus.Yap1] = self.boolean_network[Afumigatus.ROS]
        temp[Afumigatus.SOD2_3] = self.boolean_network[Afumigatus.Yap1]
        temp[Afumigatus.Cat1_2] = self.boolean_network[Afumigatus.Yap1] & (-self.boolean_network[Afumigatus.HapX] + 1)
        temp[Afumigatus.ThP] = self.boolean_network[Afumigatus.Yap1];

        temp[Afumigatus.Fe] = 0 # might change according to iron environment?
        temp[Afumigatus.O] = 0
        temp[Afumigatus.TAFCBI] = 0

        #print(self.boolean_network)
        for i in range(Afumigatus.SPECIES_NUM):
            self.boolean_network[i] = temp[i]

    def update_status(self):
        if self.status != Afumigatus.HYPHAE:
            self.iteration = self.iteration + 1
        if self.status == Afumigatus.RESTING_CONIDIA and self.iteration > Constants.ITER_TO_AFUMIGATUS_CHANGE_STATE:
            self.status = Afumigatus.SWELLING_CONIDIA
            self.iteration = 0
        elif self.status == Afumigatus.SWELLING_CONIDIA and self.iteration > Constants.ITER_TO_AFUMIGATUS_CHANGE_STATE:
            self.status = Afumigatus.HYPHAE
            self.iteration = 0

    def is_dead(self):
        #if (self.boolean_network[Afumigatus.ROS] == 1) or self.status == Afumigatus.DEAD:
        #    self.status = Afumigatus.DEAD
        #    Afumigatus.total_afumigatus = Afumigatus.total_afumigatus - 1
        #    #if self.previous_septa != None: self.previous_septa.growable = self.growable
        #    return True
        #if self.status == Afumigatus.INTERNALIZED:
        #    #Afumigatus.total_afumigatus = Afumigatus.total_afumigatus - 1
        #    return False
        return False

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

#    def selected(self, level):
#        return 1 if random() < level * level / (level * level + Constants.K * Constants.K) else 0
#
#    def activation(self, level):
#        return level * level / (level * level + Constants.K * Constants.K)

    def has_iron(self):
        self.Fe = Util.hillProbability(self.iron_pool, Constants.Kma) > random()

    def inc_iron_pool(self, qtty):
        self.iron_pool = self.iron_pool + qtty
        Afumigatus.total_iron = Afumigatus.total_iron + qtty

class Neutrophil(Cell):

    total_iron = 0
    FREE = 0
    INTERACTING = 1
    ANERGIC = 2

    def __init__(self, iron_pool):
        self.iron_pool = iron_pool
        Neutrophil.total_iron = Neutrophil.total_iron + iron_pool
        self.iteration = 0
        self.status = Neutrophil.FREE
        self.has_interacted_with_afumigatus = False

    def process_boolean_network(self):
        pass

    def update_status(self):
        if self.status == Neutrophil.INTERACTING:
            self.status == Neutrophil.ANERGIC
        if self.status == Neutrophil.ANERGIC:
            self.iteration += 1
        if self.iteration == Constants.ITER_TO_LYMPHOCYTES_CHANGE_STATE:
            self.status = Neutrophil.FREE
            self.iteration = 0

    def is_dead(self):
        return False

    def inc_iron_pool(self, qtty):
        self.iron_pool = self.iron_pool + qtty
        Neutrophil.total_iron = Neutrophil.total_iron + qtty

    def interact(self, interactable):
        if type(interactable) is Neutrophil:
            return False
        if type(interactable) is Afumigatus:
            self.status = Neutrophil.INTERACTING
            return True
        if type(interactable) is Macrophage:
            return False
        if type(interactable) is Transferrin:
            return False
        if type(interactable) is TAFC:
            return False
        if type(interactable) is Iron:
            return False
        if type(interactable) is ROS:
            return False
        return interactable.interact(self)

#    def selected(self, level):
#        return 1 if random() < level * level / (level * level + Constants.K * Constants.K) else 0
#
#    def activation(self, level):
#        return level * level / (level * level + Constants.K * Constants.K)