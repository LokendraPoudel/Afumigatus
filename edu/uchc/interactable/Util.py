class Constants():

    K = 1
    ITER_TO_CHANGE_STATE = 25
    P_BRANCH = 0.25

class Util():

    @staticmethod
    def michaelianKinetics(substract1, substract2, km):
        if substract1 > substract2:
            enzime = substract2
            substract = substract1
        else:
            enzime = substract1;
            substract = substract2;


        return enzime * substract / (substract + km);