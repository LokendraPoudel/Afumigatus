from edu.uchc.interactable.Cells import *
from random import shuffle
import random
from edu.uchc.geometry.Diffusion import *
#from edu.uchc.geometry.Model import *
from random import random, randint
#import thread

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
    def construc_model(afumigatus, macrophages, neutrophils):
        from edu.uchc.geometry.Voxel import Voxel
        xbin = 10 #40
        ybin = 10 #60
        zbin = 10 #40
        Model.grid = [[[Voxel(x, y, z) for z in range(zbin)] for y in range(ybin)] for x in range(xbin)]

        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    iron = Iron(0)
                    transferrin = Transferrin(1.0, 1.0)

                    ros = ROS(0)
                    lac = Lactoferrin(0,0)
                    tafc = TAFC(0, 0)#, lac, transferrin)

                    Model.grid[x][y][z].set_molecule("iron", iron)
                    Model.grid[x][y][z].set_molecule("tafc", tafc)
                    Model.grid[x][y][z].set_molecule("transferrin", transferrin)
                    Model.grid[x][y][z].set_molecule("ros", ros)
                    Model.grid[x][y][z].set_molecule("lactoferrin", lac)

        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    if x - 1 >= 0: Model.grid[x][y][z].neighbors.append(Model.grid[x - 1][y][z])
                    if x + 1 < 9: Model.grid[x][y][z].neighbors.append(Model.grid[x + 1][y][z])
                    if y - 1 >= 0: Model.grid[x][y][z].neighbors.append(Model.grid[x][y - 1][z])
                    if y + 1 < 9: Model.grid[x][y][z].neighbors.append(Model.grid[x][y + 1][z])
                    if z - 1 >= 0: Model.grid[x][y][z].neighbors.append(Model.grid[x][y][z - 1])
                    if z + 1 < 9: Model.grid[x][y][z].neighbors.append(Model.grid[x][y][z + 1])

        # start_time = time.time()
        # #g = Geometry(dimen["xbin"], dimen["ybin"], dimen["zbin"], data["multi_process"], data["vessel layer"])
        # with open("/Users/henriquedeassis/PycharmProjects/Afumigatus/edu/uchc/geometry/input.json") as f:
        #     data = json.load(f)
        # dimen = data["dimension"]
        # g = Geometry(dimen["xbin"], dimen["ybin"], dimen["zbin"], Model.grid, data["multi_process"], data["vessel layer"])

        # for function in data["function"]:
        #
        #     if (function["type"] == QUADRIC):
        #         f = Quadric(function)
        #         g.add(f)
        #     elif (function["type"] == VECTOR):
        #         f = Vector(function)
        #         g.add(f)

        # g.construct()
        # print("--- %s seconds ---" % (time.time() - start_time))

        for _ in range(afumigatus):
            x = randint(1,8)
            y = randint(1,8)
            z = randint(1,8)
            Model.grid[x][y][0].set_agent(Afumigatus(x=x + random(), y=y + random(), z=z+random()))
            #Model.grid[x][y][z].set_agent(Neutrophil(0.0))
        for _ in range(macrophages):
            x = randint(0, 9)
            y = randint(0, 9)
            z = randint(0, 9)
            Model.grid[x][y][0].set_agent(Macrophage(0.01))
        for _ in range(neutrophils):
            x = randint(0, 9)
            y = randint(0, 9)
            z = randint(0, 9)
            Model.grid[x][y][0].set_agent(Neutrophil(0.0))



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
    def run(iterations, file):
        print(file)
        with open(file, "w") as f:
            #print("aspergillus\tiron\tTAFC\tTAFCBI\tTf\tTfBI\tLactoferrin\tLactoferrinBI\tROS\ttotal_tf\tAfIronPool\tMphIronPool\tNeutrophilIron\tTotalIron")
            f.write("aspergillus,iron,TAFC,TAFCBI,Tf,TfBI,Lactoferrin,LactoferrinBI,ROS,total_tf,AfIronPool,MphIronPool,NeutrophilIron,TotalIron")
            f.write("\n")
            for i in range(iterations):
                for x in range(10):
                    for y in range(10):
                        for z in range(10):
                            Model.grid[x][y][z].interact()
                            Model.grid[x][y][z].update()
                            Model.grid[x][y][z].move()
                            #if i==10 and Model.has_afumigatus(Model.grid[x][y][z]):
                            #    Model.grid[x][y][z].molecules["lactoferrin"].inc(100, "Lactoferrin")
                Model.diffusion(20)
                print(i)
                #Model.print_lattice(Model.grid, i)
                f.write( \
                    str(Afumigatus.total_afumigatus) + "," + str(Iron.total_iron) + "," + str(TAFC.total_tafc[0]) + "," + str(TAFC.total_tafc[1]) + "," + \
                    str(Transferrin.total_transferrin[0]) + "," + str(Transferrin.total_transferrin[1]) + "," + \
                    str(Lactoferrin.total_lactoferrin[0]) + "," + str(Lactoferrin.total_lactoferrin[1]) + "," + str( ROS.total_ros) + "," + \
                    str((Transferrin.total_transferrin[0] + Transferrin.total_transferrin[1])) + "," + \
                    str(Afumigatus.total_iron) + "," + str(Macrophage.total_iron) + "," + str(Neutrophil.total_iron) + "," + \
                    str((Iron.total_iron + TAFC.total_tafc[1] + Transferrin.total_transferrin[1] + \
                     Afumigatus.total_iron + Macrophage.total_iron + Neutrophil.total_iron) + Lactoferrin.total_lactoferrin[1]))
                f.write("\n")
            #Model.print_statistics()

    @staticmethod
    def has_afumigatus(voxel):
        for p in voxel.interactables:
            if type(p) is Afumigatus:
                return True
        return False


    @staticmethod
    def diffusion(iterations):
        diffusion = Diffuse(0.1, 3000 / 1.4, 10)
        diffusion.solver(Model.grid, "iron", 0)
        diffusion.solver(Model.grid, "transferrin", 0)
        diffusion.solver(Model.grid, "transferrin", 1)
        diffusion.solver(Model.grid, "tafc", 0)
        diffusion.solver(Model.grid, "tafc", 1)
        diffusion.solver(Model.grid, "lactoferrin", 0)
        diffusion.solver(Model.grid, "lactoferrin", 1)

        """
        for i in range(iterations):
            for x in range(33):
                for y in range(33):
                    for z in range(1):
                        Model.diffuse(Model.grid[x][y][z])
        """

    @staticmethod
    def print_lattice(grid, ii):
        file = "/Users/henriquedeassis/Documents/Afumigatus/data/lattice_" + str(ii)
        with open(file, "w") as f:
            for i in range(33):
                line = ""
                for j in range(33):
                    line = line + "," + Model.get_number(grid[i][j][0])
                f.write(line)
                f.write("\n")

    @staticmethod
    def get_number(voxel):
        number = 0
        for p in voxel.interactables:
            if type(p) is Afumigatus:
                number = number | 1
            elif type(p) is Neutrophil:
                number = number | 2
            elif type(p) is Lactoferrin and p.get("Lactoferrin") > 0:
                number = number | 4

        return str(number)

    @staticmethod
    def diffuse(voxel):



        """
        for mol in voxel.molecules.values():
            if type(mol) is Iron:
                for v in voxel.neighbors:
                    qtty = (v.molecules["iron"].get() + mol.get())/2.0
                    mol._iron = qtty
                    v.molecules["iron"]._iron = qtty
            if type(mol) is Transferrin:
                n = len(voxel.neighbors)
                qtty = 0.25*mol.get("Tf")
                mol.dec(qtty, "Tf")
                tfqtty = qtty / n

                qtty = 0.25*mol.get("TfBI")
                mol.dec(qtty, "TfBI")
                tfbiqtty = qtty / n

                for v in voxel.neighbors:
                    v.molecules["transferrin"].inc(tfqtty, "Tf")
                    v.molecules["transferrin"].inc(tfbiqtty, "TfBI")
        """

                # for v in voxel.neighbors:
                #     qtty = (v.molecules["transferrin"].getTf() + mol.getTf())/2.0
                #     print("a")
                #     mol._tf = qtty
                #     v.molecules["transferrin"]._tf = qtty
                #     qtty = (v.molecules["transferrin"].getTfBI() + mol.getTfBI())/2.0
                #     mol._tfbi = qtty
                #     v.molecules["transferrin"]._tfbi = qtty


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
            str(Transferrin.total_transferrin[0]) + "\t" + str(Transferrin.total_transferrin[1]) + "\t" + \
            str(Lactoferrin.total_lactoferrin[0]) + "\t" + str(Lactoferrin.total_lactoferrin[1]) + "\t" + str(ROS.total_ros) + "\t" + \
            str((Transferrin.total_transferrin[0] + Transferrin.total_transferrin[1])) + "\t" + \
            str(Afumigatus.total_iron) + "\t" + str(Macrophage.total_iron) + "\t" + str(Neutrophil.total_iron) + "\t" + \
            str((Iron.total_iron + TAFC.total_tafc[1] + Transferrin.total_transferrin[1] + \
                 Afumigatus.total_iron + Macrophage.total_iron + Neutrophil.total_iron + Lactoferrin.total_lactoferrin[1])))

    @staticmethod
    def main(id):
        # Model.initial_iron_pool = 50
        # Model.iron_qtty = 0
        # Model.num_aspergillus = 0
        # Model.pre_inhalation_num = 500
        # Model.num_macrophages = 50
        # Model.transferrin_qtty = 5000
        # Model.tfbi_qtty = 5000


        Kcat = [1.0895613, 1.9075019, 0.9177211, 1.3903660, 1.2074473, 1.7247628, 1.5614466, 1.9614443, 0.9334904, 0.9780947, 1.8794019,\
                0.7622887, 1.8024647, 1.6015920, 1.1024805, 0.7786350, 1.1515664, 0.3767877, 0.6674034, 1.3568110, 1.7306366, 0.6333182,\
                1.8305048, 0.8777895, 1.5283617, 1.4828887, 1.9353435, 0.8519446, 1.5024002, 0.7319991, 1.0156286, 0.5174311, 0.8192083,\
                0.6912533, 0.3150656, 0.2509831, 0.4357868, 1.2415306, 1.0554773, 1.0075806, 0.2002724, 0.5670968, 0.3482853, 0.4929708,\
                1.9811518, 1.4495878, 1.6697206, 0.5939810, 1.7704696, 0.4596072, 0.5438018, 1.6897095, 0.2894513, 1.6153523, 1.2966023,\
                1.3168466, 1.1811365, 0.3859438, 1.2648964, 1.4016441]
        Km = [19.659841, 12.149579, 11.475613, 8.067452,  19.918429,  5.369286, 12.691719,  7.854368,  8.551788, 10.099183,  7.091322,\
              17.835488, 17.407521, 11.173349, 2.221452,  13.335059, 18.542585, 13.654878,  2.548324, 14.133144,  3.956695, 10.515239,\
               6.979062,  3.124822, 18.472618, 11.652067,  2.720007, 15.401185, 12.410839, 18.099902, 10.835164,  9.412489, 16.041283,\
               4.555363,  8.947056, 14.467935,  3.569655, 14.632251,  6.034135,  4.345148, 13.020329,  9.598083, 16.348810, 17.010228,\
               3.481538,  7.524477,  5.188764, 15.618009,  5.770968,  6.501902, 19.271102, 10.300338,  7.102509,  6.219771,  8.687950,\
              16.462906 ,18.875139, 14.949694,  4.722851, 13.762914]
        Kma = [12.636689,  7.859848,  9.234812, 11.055524, 16.824120,  5.340810, 13.677214,  6.219970,  5.910021,  6.933457, 10.712566,\
               15.423526, 18.108073,  6.686905,  2.050811, 10.023224, 16.193003, 16.553607, 12.869024,  3.961401,  8.121547,  7.317636,\
                3.172055, 11.893202, 17.607942, 17.254790,  8.885166, 14.678822, 15.664887, 18.899287, 19.798026, 19.208694, 18.512852,\
                3.784882,  5.004894, 13.122027, 17.593691, 18.418099, 10.145450,  9.548723,  4.666488, 19.615763, 14.523205,  8.415356,\
                3.313182, 14.215120, 12.327658,  7.511928, 13.924428, 10.502152, 11.377240,  9.097549,  4.754750,  5.685903,  2.667449,\
               12.008212,  4.194153, 16.029830,  2.407089, 15.072778]
        IAF = [32, 28, 14,  8, 25, 26, 12, 11,  8, 23, 28, 16, 36, 40, 16, 35, 38, 29, 34,  5, 17, 15, 37,  7, 36, 19, 24, 35, 31, 29, 21,\
               32, 27, 15, 34,  9, 20, 21, 24,  9, 22, 19, 39, 31, 13, 22,  6, 10,  7, 17,  6, 26, 39, 12, 30, 13, 18, 25, 33, 39]
        IM = [6, 15, 19, 13, 10, 10,  4, 18,  7,  9, 13,  9,  3, 15, 12,  3,  3,  9,  5, 19, 10, 14,  6, 12,  5, 13,  4, 15, 17,  8,  7, 11,\
              8, 16,  5, 14, 20, 18,  8, 17, 11,  4,  6, 15, 12, 11,  4,  6, 19, 12, 14, 16, 10, 20, 18, 20, 16, 17, 18,  8]
        Pb = [0.07928711, 0.17038405, 0.35319508, 0.27271324, 0.31749857, 0.35886097, 0.33432877, 0.43924803, 0.26675114, 0.49512588,\
              0.44087916, 0.43088249, 0.11800540, 0.19458943, 0.12901790, 0.30838445, 0.38482417, 0.37191395, 0.25846768, 0.44951689,\
              0.05587233, 0.45847064, 0.34323902, 0.25038630, 0.15399596, 0.47672721, 0.32703630, 0.10604947, 0.48622083, 0.14483689,\
              0.11551638, 0.20870467, 0.09762051, 0.40846591, 0.28425985, 0.22926607, 0.13270075, 0.41532431, 0.39872548, 0.20068395,\
              0.22192791, 0.24060129, 0.15874724, 0.08353441, 0.37727183, 0.47906387, 0.18419151, 0.27776919, 0.33630001, 0.06105336,\
              0.29296018, 0.18870145, 0.30003436, 0.23002629, 0.41854100, 0.46647455, 0.39365860, 0.08804473, 0.16427430, 0.07162650]
        Pmup = [0.03108568, 0.07478623, 0.05545106, 0.12897802, 0.05055302, 0.07256868, 0.19099792, 0.10895204, 0.11185397, 0.08553290,\
               0.15255608, 0.16064708, 0.17295532, 0.14354498, 0.09880311, 0.10698726, 0.10295047, 0.15048262, 0.19799570, 0.12372486,\
               0.07956069, 0.03860554, 0.14222136, 0.04499278, 0.05801602, 0.11807365, 0.04855042, 0.09708931, 0.13942793, 0.09184408,\
               0.06258459, 0.17528282, 0.13614084, 0.06021267, 0.06584711, 0.02687663, 0.03449621, 0.11372938, 0.16118740, 0.14660873,\
               0.16716445, 0.07089608, 0.09423767, 0.18556872, 0.08096394, 0.13390480, 0.17902925, 0.02431168, 0.17848916, 0.19212080,\
               0.18495260, 0.12069042, 0.02223655, 0.16696426, 0.15623222, 0.19573938, 0.12567845, 0.03527189, 0.08810781, 0.04317900]
        Pqup = []
        base = [0.17047734, 0.02326142, 0.09148356, 0.15329397, 0.14379736, 0.17771164, 0.08173570, 0.10878692, 0.19090793, 0.02713361,\
                0.19573390, 0.07054574, 0.08507241, 0.13175570, 0.06537707, 0.14279062, 0.08761121, 0.06050580, 0.11300940, 0.04598130,\
                0.09868317, 0.15558276, 0.13892358, 0.04789205, 0.05095201, 0.18150498, 0.04344479, 0.07211463, 0.18239637, 0.12382146,\
                0.05664685, 0.12651730, 0.14640570, 0.13615170, 0.10695470, 0.16662585, 0.16225343, 0.11136412, 0.12006963, 0.11878014,\
                0.02256308, 0.09699995, 0.16948018, 0.12925622, 0.10295855, 0.05594042, 0.09404843, 0.14991664, 0.19130040, 0.03164314,\
                0.17355506, 0.06486815, 0.03334563, 0.07547396, 0.15910608, 0.04087152, 0.18544659, 0.19760460, 0.07979126, 0.03685374]
        lac = [18.940371,  8.024040, 16.520740, 13.197346, 17.664413, 17.538253,  9.463773, 10.188773, 19.766311, 11.306915, 17.269104,\
               15.378469, 10.491563, 13.947108,  3.624228, 18.218625, 15.558197, 13.435677, 12.661897,  3.813828, 15.974230,  8.425288,\
                7.280008,  5.039500,  6.996397,  8.639940,  7.493395,  9.064346,  2.921284, 16.706264,  4.704772, 14.330251,  5.359672,\
               19.580546,  7.748062, 10.952168,  6.063125, 11.859276, 14.131997,  6.553445, 12.057257,  3.207131,  9.738361,  4.616052,\
               17.900133,  4.362100,  2.837182,  2.073300, 16.191243,  5.810760, 12.462428, 14.728707,  2.306323, 18.562210,  6.239102,\
               19.140906,  9.929763, 11.257238, 15.113830, 12.888178]


        filename = "/Users/henriquedeassis/Documents/Afumigatus/data/simulation"


        f = open("/Users/henriquedeassis/Documents/Afumigatus/data/lhs.csv", "r")
        j = 0
        #for i in range(60):

        for line in f:
            j = j + 1
            sp = line.split(",")
            Model.aspergillus_count = 0
            Model.macrophage_iron_pool = 0
            Model.aspergilus_iron_pool = 0
            Model.transferrin_qtty = 0.0
            Model.tfbi_qtty = 0.0
            Model.iron_qtty = 0.0
            Model.initial_iron_pool = 0.0
            Model.num_macrophages = 0
            Model.num_aspergillus = 0
            Model.pre_inhalation_num = 0
            Model.iron = None
            Model.tafc = None
            Model.tafcbi = None
            Model.tf = None
            Model.tfbi = None
            Model.interactables = []
            Model.tmp = []
            Model.grid = None
            Iron.total_iron = 0
            Macrophage.total_iron = 0
            Afumigatus.total_iron = 0
            Afumigatus.total_afumigatus = 0
            TAFC.total_tafc = [0, 0]
            Transferrin.total_transferrin = [0, 0]
            ROS.total_ros = 0
            Lactoferrin.total_lactoferrin = [0, 0]

            Constants.Kcat = float(sp[0])
            Constants.Km = float(sp[1])
            Constants.Kma = float(sp[2])
            Constants.ITER_TO_AFUMIGATUS_CHANGE_STATE = float(sp[3])
            Constants.ITER_TO_LYMPHOCYTES_CHANGE_STATE = float(sp[4])
            Constants.P_BRANCH = float(sp[5])
            Constants.MPH_UPTAKE_QTTY = float(sp[6])
            Constants.AF_UPTAKE_QTTY = float(sp[7])
            Constants.TAFC_QTTY = float(sp[8])
            Constants.LAC_QTTY = float(sp[9])
            print((Constants.Kcat, Constants.Km, Constants.Kma, Constants.ITER_TO_AFUMIGATUS_CHANGE_STATE, \
                   Constants.ITER_TO_LYMPHOCYTES_CHANGE_STATE, Constants.P_BRANCH, Constants.MPH_UPTAKE_QTTY, \
                   Constants.AF_UPTAKE_QTTY, Constants.TAFC_QTTY, Constants.LAC_QTTY))
            Model.construc_model(50, 0, 0)
            Model.run(200, filename + "_" + str(j) + ".csv")
        f.close()


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
    for i in range(1):
        Model.main(str(i))

    '''''
    for m in [50, 100, 250, 500]:
        for n in [50, 100, 250, 500]:
            for i in range(3):
                Model.aspergillus_count = 0
                Model.macrophage_iron_pool = 0
                Model.aspergilus_iron_pool = 0
                Model.transferrin_qtty = 0.0
                Model.tfbi_qtty = 0.0
                Model.iron_qtty = 0.0
                Model.initial_iron_pool = 0.0
                Model.num_macrophages = 0
                Model.num_aspergillus = 0
                Model.pre_inhalation_num = 0
                Model.iron = None
                Model.tafc = None
                Model.tafcbi = None
                Model.tf = None
                Model.tfbi = None
                Model.interactables = []
                Model.tmp = []
                Model.grid = None
                Iron.total_iron = 0
                Macrophage.total_iron = 0
                Afumigatus.total_iron = 0
                Afumigatus.total_afumigatus = 0
                TAFC.total_tafc = [0,0]
                Transferrin.total_transferrin = [0,0]
                ROS.total_ros = 0
                Lactoferrin.total_lactoferrin = [0,0]


                Model.construc_model(m, n)
                Model.run(750, filename + str(i) + "_" + str(ros) + "_" + str(lac) + ".csv")
'''''
