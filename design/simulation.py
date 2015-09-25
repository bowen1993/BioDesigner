"""
simulation.py implement the simulation function

@author: Bowen
"""

import math
import random
import copy

class reaction_simulator:
    """
    reaction simulator
    """
    def __init__(self, reaction_list, martial_list, reaction_time=200):
        """
        init function

        @param reaction_list: reactions
        @type reaction_list: list
        @param martial_list : init materials
        @type martial_list: list
        @param reaction_time: the reaction time
        @type reaction_time: int
        """
        self.compound_pool = dict()
        self.reactions = list()
        self.history = dict()
        self.currentTime = 0
        for martial in martial_list:
            self.compound_pool[martial[0]] = int(martial[1])
        for reaction in reaction_list:
            reaction['k'] = float(reaction['k'])
            for reactant in reaction['reactants']:
                if reactant not in self.compound_pool.keys():
                    self.compound_pool[reactant] = 0
            for product in reaction['products']:
                if product not in self.compound_pool.keys():
                    self.compound_pool[product] = 0
            self.reactions.append(reaction)
        self.history[self.currentTime] = copy.deepcopy(self.compound_pool)
        self.reaction_time = reaction_time

    def __get_compound_amount(self, t, compound):
        """
        compound amount at time t

        @param t: time point
        @type t: int
        @param compound: compound name
        @type compound: str
        @return: amount of compound
        @rtype:int
        """
        if t == self.currentTime:
            return self.compound_pool[compound]
        elif t > self.currentTime:
            return None
        else:
            while t >= 0:
                if t in self.history.keys():
                    return self.history[t][compound]
                t -= 1
            return self.compound_pool[compound]


    def calA(self, reaction):
        """
        cal a in SSA

        @param reaction: reaction to cal with
        @type reaction: dict
        @return : a0
        @rtype: float
        """
        result = reaction['k']
        lastItem = ''
        for reactant in reaction['reactants']:
            if reactant == lastItem:
                result *= self.__get_compound_amount(self.currentTime-1, reactant)
            else:
                result *= self.__get_compound_amount(self.currentTime, reactant)
            lastItem = reactant
        return result

    def __calItoJ(self, i, j):
        result = 0
        for index in range(i, j+1):
            result += self.calA(self.reactions[index])
        return result

    def calA0(self):
        result = 0
        for reaction in self.reactions:
            result += self.calA(reaction)
        return result

    def calTT(self, a0, r1):
        """
        cal when reaction happens

        @param a0 : a0 in SSA
        @type a0: int
        @param r1: random number
        @type r1: float
        @return : reaction happend time point
        @rtype: float
        """
        tt = (1.0 / a0) * math.log((1.0/r1))
        return tt

    def doReaction(self, index):
        """
        make reaction happens

        @param index: reaction index
        @type index: int
        """
        reaction = self.reactions[index]
        for reactant in reaction['reactants']:
            self.compound_pool[reactant] -= 1
        for product in reaction['products']:
            self.compound_pool[product] += 1

    def __isJOccurs(self, j, a0, r2):
        leftBound = (1.0/a0)*self.__calItoJ(0, j-1)
        rightBound = (1.0/a0)*self.__calItoJ(0, j)
        if leftBound <= r2 < rightBound and self.isReactantReady(j):
            return True
        else:
            return False

    def isReactantReady(self, j):
        reaction = self.reactions[j]
        for reactant in reaction['reactants']:
            if self.compound_pool[reactant] < 1:
                return False
        return True

    def doSimulation(self):
        """
        simulate the reaction
        """
        while self.reaction_time > 0:
            r1 = random.random()
            r2 = random.random()
            if r1 == 0:
                r1 = 0.0000001
            if r2 == 0:
                r2 = 0.0000001
            a0 = self.calA0()
            if a0 == 0:
                a0 = 0.0000001
            tt = self.calTT(a0, r1)
            self.reaction_time -= tt
            for i in range(len(self.reactions)):
                if self.__isJOccurs(i, a0, r2):
                    self.doReaction(i)
            self.currentTime += tt
            self.history[self.currentTime] = copy.deepcopy(self.compound_pool)

    def form_result(self):
        formed_result = list()
        for key in self.history:
            compound_index = 0
            for comp in self.history[key]:
                item_info = {
                    'date': key,
                    'pv' : self.history[key][comp],
                    'name' : comp,
                    'order' : compound_index,
                }
                formed_result.append(item_info)
                compound_index += 1
        return sorted(formed_result, key=lambda x: (x['order'] ,x['date']))

    def getProcess(self):
        """
        get the simulate result

        @return: simulate result
        @rtype: list
        """
        return self.form_result()


