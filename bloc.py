import random
from random import randint
import time
import copy



def print_list(list):
    for l in list:
        print("| ", l , end=" | ")
    print("\n")

def get_remove(l):
    selection = random.choice(l)
    l.remove(selection)

    return selection

def get_emp(emp):
    tmp = emp
    while tmp == emp:
        tmp = randint(0,2)
    return tmp

class Bloc:

    def __init__(self, pos_ini, pos_fin,name):
        self.pos_ini = pos_ini
        self.pos_final = pos_fin
        self.pos_act = pos_ini
        self.satisfaction = True if self.pos_ini == self.pos_final else False
        self.blocT = None
        self.blocD = None
        self.name = name
        
    def __str__(self):
     return self.name

    def perception(self,env):
        infos = env.get_infos(self)
        print(" Am I ", self ,"pushed : ", infos["pushed"])
        self.blocT = infos["blocT"]
        self.blocD = infos["blocD"]
        self.pos_act = infos["pos"]
        self.emplacement = infos["emp"]
        self.satisfaction = True if self.pos_act == self.pos_final else False
        self.statisfaction = self.satisfaction if infos["pushed"] != True else False


    def actions(self,env):
        print("Im ", self, "satisfied : ",self.satisfaction, " pos : ",self.pos_act, " Goal : ",self.pos_final)
        if  not self.satisfaction and self.blocT ==None:
            self.__move(env)
        elif not self.satisfaction and self.blocT != None:
            self.__push(env)


    def __move(self,env):
        env.move(self)

    def __push(self,env):
        env.push(self)


class Environment:

    def __init__(self,n):
        self.blocs = []
        self.conf_int = [i for i in range(n)]
        self.conf_fin = [i for i in range(n)]
        
        for i in range(n):
            self.blocs.append(Bloc(get_remove(self.conf_int),get_remove(self.conf_fin),"B"+str(i)))
        self.blocs.sort(key=lambda x: x.pos_ini)
        self.signals = []
        self.emplacements = [[ i for i in self.blocs],[],[]]
        

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
        elif pos == len(self.emplacements[emp])-1:
            return (self.emplacements[emp][pos-1],None)
        
        return (self.emplacements[emp][pos-1],self.emplacements[emp][pos+1])

    def move(self,bloc):
        emp = bloc.emplacement
        tmp = get_emp(emp)
        self.emplacements[emp].pop()
        self.emplacements[tmp].append(bloc)
        print("Im : ",bloc.name, " moved to : ",tmp)
        if bloc in self.signals:
            self.signals.remove(bloc)
    
    def push(self,bloc):
        if bloc.blocT not in self.signals:
            self.signals.append(bloc.blocT)
            print("Im : ",bloc.name, " Pushing : ",bloc.blocT)
    

    def ok(self):
        sat = 0
        for bloc in self.blocs:
            sat += bloc.satisfaction
        return True if sat == len(self.blocs) else False


def main():
    env = Environment(4)
    for b in env.blocs:
        print("Im : ", b ,env.get_infos(b)," pos_final ", b.pos_final, " and pos_ini",b.pos_ini)
    while(not env.ok()):
        for bloc in env.blocs:
            bloc.perception(env)
            bloc.actions(env)
        print("\n ----------------------------------------------")
        for idx, val in enumerate(env.emplacements):
            print("Emp : ", idx, end=" ")
            print_list(val)
        print("---------------------------------------------- \n")
        
        print("signals : ", end=" ")
        print_list(env.signals)
        print("\n")
        print("I have : ", len(env.blocs), " Blocs")
        time.sleep(1)
        print("\n")


if __name__ == "__main__":
    main()
