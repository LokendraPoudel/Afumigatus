import numpy as np
import math

class Constants():

    Kcat = 1
    Km = 10
    Kma = 10
    ITER_TO_AFUMIGATUS_CHANGE_STATE = 25
    ITER_TO_LYMPHOCYTES_CHANGE_STATE = 10
    P_BRANCH = 0.25
    MPH_UPTAKE_QTTY = 0.1
    AF_UPTAKE_QTTY = 0.1
    TAFC_QTTY = 0.1
    LAC_QTTY = 1
    #LAC = 10

    #ROS_QTTY  = 0 * BASE_QTTY
    #LAC_QTTY  = LAC * BASE_QTTY
    #TAFC_QTTY = 1 * BASE_QTTY

    def __init__(self, Kcat, Km, Kma, ITER_TO_AFUMIGATUS_CHANGE_STATE, ITER_TO_LYMPHOCYTES_CHANGE_STATE, P_BRANCH, UPTAKE_QTTY, BASE_QTTY, LAC):
        Constants.Kcat = Kcat
        Constants.Km = Km
        Constants.KMa = Kma
        Constants.ITER_TO_AFUMIGATUS_CHANGE_STATE = ITER_TO_AFUMIGATUS_CHANGE_STATE
        Constants.ITER_TO_LYMPHOCYTES_CHANGE_STATE = ITER_TO_LYMPHOCYTES_CHANGE_STATE
        Constants.P_BRANCH = P_BRANCH
        Constants.UPTAKE_QTTY = UPTAKE_QTTY
        Constants.BASE_QTTY = BASE_QTTY
        Constants.LAC = LAC

        print((Constants.Kcat, Constants.Km, Constants.Kma, Constants.ITER_TO_AFUMIGATUS_CHANGE_STATE, \
               Constants.ITER_TO_LYMPHOCYTES_CHANGE_STATE, Constants.P_BRANCH, Constants.UPTAKE_QTTY, \
               Constants.BASE_QTTY, Constants.LAC))


class Util():

    cosTheta = math.cos(math.pi/4.0)
    sinTheta = math.sin(math.pi / 4.0);

    @staticmethod
    def michaelianKinetics(substract1, substract2, km = Constants.Km, Kcat = Constants.Kcat):
        if substract1 > substract2:
            enzime = substract2
            substract = substract1
        else:
            enzime = substract1;
            substract = substract2;


        return Kcat * enzime * substract / (substract + km)

    def hillProbability(substract, km = Constants.Km):
        return substract * substract / (substract * substract + km * km)

    @staticmethod
    def solver(mol1, mol2, h):
        if(mol1 > mol2):
            substract = mol1
            enzime = mol2
        else:
            substract = mol2
            enzime = mol1

        v = h * enzime * substract / (substract + Constants.K)
        enzime = enzime - v
        substract = substract - v
        return (h / 2) * (v + enzime * substract / (substract + Constants.K))

    @staticmethod
    def rotatation_matrix(phi):
        return np.array([[Util.cosTheta * math.cos(phi), -Util.cosTheta*math.sin(phi), Util.sinTheta],\
                         [math.sin(phi), math.cos(phi), 0.0],\
                         [-Util.sinTheta*math.cos(phi), Util.sinTheta*math.sin(phi), Util.cosTheta]])
