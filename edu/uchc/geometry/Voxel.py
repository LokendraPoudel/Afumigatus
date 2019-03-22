from random import shuffle
import random

class Voxel():
    AIR = 0
    EPITHELIUM = 1
    REGULAR_TISSUE = 2
    BLOOD = 3

    aspergillus_count = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.type = Voxel.AIR
        self.interactables = []
        self.neighbors = []

    def set_agents(self, interactables):
        self.interactables = interactables

    def set_type(self, type):
        self.type = type

    def set_agent(self, interactable):
        self.interactables.append(interactable)

    def set_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def interact(self):
        shuffle(self.interactables)
        size = len(self.interactables)
        for i in range(size):
            for j in range(i, size):
                a1 = self.interactables[i]
                a2 = self.interactables[j]
                a1.interact(a2)

    def update(self):
        from edu.uchc.interactable.Cells import Afumigatus
        size = len(self.interactables)
        tmp = []
        i = 0
        while i < size:
            if hasattr(self.interactables[i], "update_status"):
                self.interactables[i].update_status()
            if hasattr(self.interactables[i], "process_boolean_network"):
                self.interactables[i].process_boolean_network()
            if type(self.interactables[i]) is Afumigatus:
                if self.interactables[i].status == Afumigatus.DEAD:
                    self.interactables.pop(i)
                    size = size - 1
                    continue
                new_a = self.interactables[i].branch()
                if new_a != self.interactables[i]:
                    tmp.append(new_a)

                new_a = self.interactables[i].elongate()
                if new_a != self.interactables[i]:
                    tmp.append(new_a)
            i = i + 1
        self.interactables.extend(tmp)

    def move(self):
        from edu.uchc.interactable.Cells import Macrophage

        size = len(self.interactables)
        i = 0
        while i < size:
            index = random.randint(0, len(self.neighbors))
            if type(self.interactables[i]) is Macrophage and index != len(self.neighbors):
                m = self.interactables.pop(i)
                self.neighbors[index].interactables.append(m)
                size = size - 1
            i = i + 1
