class Constants():
    InitAfumigatusBooleanState = [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    InitMacrophageBooleanState = [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1]
    BASE_QTTY = 0.1
    KM = 10
    ITER_TO_CHANGE_STATE = 15
    MACROPHAGE_AFUMIGAUTS_ITER_PROB = 0.1
    P_BRANCH = 0.25

class Util():

    @staticmethod
    def michaelianKinetics(substract1, substract2, km):
        enzime = None
        substract = None
        if substract1 > substract2:
            enzime = substract2
            substract = substract1
        else:
            enzime = substract1;
            substract = substract2;


        return enzime * substract / (substract + km);