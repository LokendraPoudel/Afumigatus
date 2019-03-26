from edu.uchc.interactable.Cells import *
from random import shuffle
import random
from random import random, randint

class Model():
    aspergillus_count = 0
    macrophage_iron_pool = 0.0
    aspergilus_iron_pool = 0.0

    transferrin_qtty = 0.0
    tfbi_qtty = 0.0
    iron_qtty = 0.0
    initial_iron_pool = 0.0

    num_macrophages = 0
    num_aspergillus = 0
    pre_inhalation_num = 0

    iron = None
    tafc = None
    tafcbi = None
    tf = None
    tfbi = None
    interactables = [] #agents
    tmp = []
    grid = None

    # @staticmethod
    # def construc_model():
    #     Model.iron = Iron(Model.iron_qtty)
    #     Model.tfbi = TransferrinBI(Model.tfbi_qtty);
    #     Model.tf = Transferrin(Model.tfbi, Model.transferrin_qtty);
    #     Model.tafcbi = TAFCBI(0.0);
    #     Model.tafc = TAFC(Model.tafcbi, Model.tf, 0.0);
    #
    #     Model.interactables.append(Model.iron)
    #     Model.interactables.append(Model.tfbi)
    #     Model.interactables.append(Model.tf)
    #     Model.interactables.append(Model.tafc)
    #     Model.interactables.append(Model.tafcbi)
    #     for i in range(Model.num_macrophages):
    #         m = Macrophage(Model.iron, Model.tfbi, Model.tf)
    #         m.iron_pool = Model.initial_iron_pool
    #         Model.interactables.append(m)
    #     #Model.print_statistics()

    @staticmethod
    def construc_model():
        from edu.uchc.geometry.Voxel import Voxel
        Model.grid = [[[Voxel(x, y, z) for z in range(10)] for y in range(10)] for x in range(10)]

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    iron = Iron(0)
                    transferrin = Transferrin(100, 100)
                    tafc = TAFC(0, 0)
                    ros = ROS(0)

                    Model.grid[x][y][z].set_molecule("iron", iron)
                    Model.grid[x][y][z].set_molecule("tafc", tafc)
                    Model.grid[x][y][z].set_molecule("transferrin", transferrin)
                    Model.grid[x][y][z].set_molecule("ros", ros)

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    if x - 1 >= 0: Model.grid[x][y][z].neighbors.append(Model.grid[x - 1][y][z])
                    if x + 1 < 10: Model.grid[x][y][z].neighbors.append(Model.grid[x + 1][y][z])
                    if y - 1 >= 0: Model.grid[x][y][z].neighbors.append(Model.grid[x][y - 1][z])
                    if y + 1 < 10: Model.grid[x][y][z].neighbors.append(Model.grid[x][y + 1][z])
                    if z - 1 >= 0: Model.grid[x][y][z].neighbors.append(Model.grid[x][y][z - 1])
                    if z + 1 < 10: Model.grid[x][y][z].neighbors.append(Model.grid[x][y][z + 1])

        for _ in range(500):
            x = randint(1,8)
            y = randint(1,8)
            z = randint(1,8)
            Model.grid[x][y][z].set_agent(Afumigatus(x=x + random(), y=y + random(), z=z+random()))
        for _ in range(50):
            x = randint(0, 9)
            y = randint(0, 9)
            z = randint(0, 9)
            Model.grid[x][y][z].set_agent(Macrophage(0.01))



    # @staticmethod
    # def inhalate_spore(num):
    #     for i in range(num):
    #         Model.interactables.append(Afumigatus(Model.iron, Model.tafc, Model.tafcbi))

    # @staticmethod
    # def run(iterations):
    #     Model.inhalate_spore(Model.pre_inhalation_num)
    #     print("aspergillus\tiron transferrin\ttfbi\ttafc\ttafcbi\taspergilusIronPool\tmacrophageIronPool\tTotalIron")
    #     for i in range(iterations):
    #         Model.aspergilus_iron_pool = 0.0
    #         Model.macrophage_iron_pool = 0.0
    #         Model.aspergillus_count = 0
    #
    #         #Model.inhalete_spore(num)
    #         Model.interact()
    #         Model.update_agents()
    #         Model.print_statistics()

    @staticmethod
    def run(iterations):
        print("aspergillus\tiron\tTAFC\tTAFCBI\tTf\tTfBI\tROS\ttotal_tf\tAfIronPool\tMphIronPool\tTotalIron")
        for i in range(iterations):
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        Model.grid[x][y][z].interact()
                        Model.grid[x][y][z].update()
                        Model.grid[x][y][z].move()
            Model.diffusion(20)
            Model.print_statistics()

    @staticmethod
    def diffusion(iterations):
        for i in range(iterations):
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        Model.diffuse(Model.grid[x][y][z])

    @staticmethod
    def diffuse(voxel):
        for mol in voxel.molecules:
            if type(mol) is Iron:
                for v in voxel.neighbors:
                    qtty = (v.molecules["iron"].get() + mol.get())/2.0
                    mol._iron = qtty
                    v.molecules["iron"]._iron = qtty
            if type(mol) is Transferrin:
                for v in voxel.neighbors:
                    qtty = (v.molecules["transferrin"].getTf() + mol.getTf())/2.0
                    mol._tf = qtty
                    v.molecules["transferrin"]._tf = qtty
                    qtty = (v.molecules["transferrin"].getTfBI() + mol.getTfBI())/2.0
                    mol._tfbi = qtty
                    v.molecules["transferrin"]._tfbi = qtty
            # if type(mol) is ROS:
            #     for v in voxel.neighbors:
            #         qtty = (v.molecules["ros"].get() + mol.get())/2.0
            #         mol._ros = qtty
            #         v.molecules["ros"]._ros = qtty
            # if type(mol) is TAFC:
            #     for v in voxel.neighbors:
            #         qtty = (v.molecules["tafc"].getTafc() + mol.getTafc())/2.0
            #         mol._tafc = qtty
            #         v.molecules["tafc"]._tafc = qtty
            #         qtty = (v.molecules["tafc"].getTafcbi() + mol.getTafcbi())/2.0
            #         mol._tafcbi = qtty
            #         v.molecules["tafc"]._tafcbi = qtty


    # @staticmethod
    # def interact():
    #     shuffle(Model.interactables)
    #     size = len(Model.interactables)
    #     for i in range(size):
    #         for j in range(i, size):
    #             a1 = Model.interactables[i]
    #             a2 = Model.interactables[j]
    #             a1.interact(a2)

    @staticmethod
    def print_statistics():
        print(str(Afumigatus.total_afumigatus) + "\t" + str(Iron.total_iron) + "\t" + str(TAFC.total_tafc[0]) + "\t" + str(TAFC.total_tafc[1]) + "\t" + \
            str(Transferrin.total_transferrin[0]) + "\t" + str(Transferrin.total_transferrin[1]) + "\t" + str(ROS.total_ros) + "\t" + \
            str((Transferrin.total_transferrin[0] + Transferrin.total_transferrin[1])) + "\t" + \
            str(Afumigatus.total_iron) + "\t" + str(Macrophage.total_iron) + "\t" + \
            str((Iron.total_iron + TAFC.total_tafc[1] + Transferrin.total_transferrin[1] + Afumigatus.total_iron + Macrophage.total_iron)))


    # @staticmethod
    # def print_statistics():
    #     print(str(Model.aspergillus_count) + "\t" + str(Model.iron.get()) + "\t" + str(Model.tf.get()) + "\t" + \
    #           str(Model.tfbi.get()) + "\t" + str(Model.tafc.get()) + "\t" + str(Model.tafcbi.get()) + "\t" + \
    #           str(Model.aspergilus_iron_pool) + "\t" + str(Model.macrophage_iron_pool) + "\t" + \
    #           str(Model.iron.get() + Model.tfbi.get() + Model.tafcbi.get() + Model.aspergilus_iron_pool + Model.macrophage_iron_pool))

    # @staticmethod
    # def update_agents():
    #     from edu.uchc.interactable.Cells import Macrophage, Afumigatus
    #     size = len(Model.interactables)
    #     del Model.tmp[:]
    #     i = 0
    #     while i < size:
    #         agent = Model.interactables[i]
    #         if type(agent) is Macrophage:
    #             Model.update_macrophage(agent)
    #         if type(agent) is Afumigatus:
    #             new_agent = Model.update_afumigatus(agent)
    #             if agent.status == Afumigatus.DEAD:
    #                 Model.interactables.pop(i)
    #                 Model.aspergillus_count = Model.aspergillus_count - 1
    #                 size = size - 1
    #             else:
    #                 Model.aspergilus_iron_pool = Model.aspergilus_iron_pool + agent.iron_pool
    #                 if new_agent != None:
    #                     Model.aspergilus_iron_pool = Model.aspergilus_iron_pool + new_agent.iron_pool
    #         i = i + 1
    #
    #     Model.interactables.extend(Model.tmp)

    # @staticmethod
    # def update_macrophage(m):
    #     m.process_boolean_network()
    #     m.secrete_iron()
    #     Model.macrophage_iron_pool = Model.macrophage_iron_pool + m.iron_pool
    #
    # @staticmethod
    # def update_afumigatus(a):
    #     Model.aspergillus_count = Model.aspergillus_count + 1
    #
    #     new_a = a.branch()
    #     r = None
    #     if new_a != a:
    #         Model.aspergillus_count = Model.aspergillus_count + 1
    #         Model.tmp.append(new_a)
    #         r = new_a
    #
    #     new_a = a.elongate()
    #     if new_a != a:
    #         Model.aspergillus_Count = Model.aspergillus_count + 1
    #         Model.tmp.append(new_a)
    #         r = new_a
    #
    #     a.process_boolean_network()
    #     a.secrete_tafc()
    #     a.update_status()
    #     #a.diffuse_iron()
    #
    #    return r

if __name__ == "__main__":
    # Model.initial_iron_pool = 50
    # Model.iron_qtty = 0
    # Model.num_aspergillus = 0
    # Model.pre_inhalation_num = 500
    # Model.num_macrophages = 50
    # Model.transferrin_qtty = 5000
    # Model.tfbi_qtty = 5000

    Model.construc_model()
    Model.run(750)
