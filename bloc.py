import random

def get_remove(l):
    selection = random.choice(l)
    l.remove(selection)

    return selection


class Bloc:

    def __init__(self, pos_ini, pos_fin):
        self.pos_ini = pos_ini
        self.pos_final = pos_fin
        self.pos_act = pos_ini
        self.satisfaction = True if self.pos_ini == self.pos_final else False
        self.blocT = None
        self.blocD = None
        
        

    def perception(self,env):
        infos = env.get_infos(self)
        self.statisfaction = self.satisfaction if infos["pushed"] != True else False
        self.blocT = infos["blocT"]
        self.blocD = infos["blocD"]
        self.pos_act = infos["pos"]
        self.emplacement = infos["emp"]

    def actions(self):
        pass

    def __move(self,x):
        pass

    def __push():
        pass


class Environment:

    def __init__(self,n):
        self.blocs = []
        self.conf_int = [i for i in range(n)]
        self.conf_fin = [i for i in range(n)]
        
        for i in range(n):
            self.blocs.append(Bloc(get_remove(self.conf_int),get_remove(self.conf_fin)))
        self.signals = []
        self.emplacements = [self.blocs,[],[]]

    def get_infos(self,bloc):
        emp,pos = self.__get_pos(bloc)
        blocD,blocT = self.__get_top_down(emp,pos)
        pushed = bloc in self.signals

        return {"pushed":pushed,"blocD":blocD,"blocT":blocT,"emp":emp,"pos":pos}


    def __get_pos(self,bloc):
        for emp in range(3):
            for b in range(len(self.emplacements[emp])):
                if bloc == self.emplacements[emp][b]:
                    return (emp,b)

    def __get_top_down(self,emp,pos):
        if pos == 0 and len(self.emplacements[emp])==1:
            return (None,None)
        elif pos == 0 and len(self.emplacements[emp])>1:
            return (None,self.emplacements[emp][pos+1])
        elif pos == len(self.emplacements[emp]):
            return (self.emplacements[emp][pos-1],None)
        
        return (self.emplacements[emp][pos],self.emplacements[emp][pos])
            


def main():
    env = Environment(4)
    for b in env.blocs:
        print("Im : ", b ,env.get_infos(b)," b ", b.pos_final, " and ",b.pos_ini)

if __name__ == "__main__":
    main()
