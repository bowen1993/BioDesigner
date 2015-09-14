import math
import random
import copy

class reaction_simulator:
    def __init__(self, reaction_list, martial_list, reaction_time=100):
        self.compound_pool = dict()
        self.reactions = list()
        self.history = dict()
        self.currentTime = 0
        for martial in martial_list:
            self.compound_pool[martial[0]] = martial[1]
        for reaction in reaction_list:
            for reactant in reaction['reactants']:
                if reactant not in self.compound_pool.keys():
                    self.compound_pool[reactant] = 0
            for product in reaction['products']:
                if product not in self.compound_pool.keys():
                    self.compound_pool[product] = 0
            self.reactions.append(reaction)
        self.history[self.currentTime] = copy.deepcopy(self.compound_pool)
        self.reaction_time = reaction_time

    def get_compound_amount(self, t, compound):
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
        result = reaction['k']
        lastItem = ''
        for reactant in reaction['reactants']:
            if reactant == lastItem:
                result *= self.get_compound_amount(self.currentTime-1, reactant)
            else:
                result *= self.get_compound_amount(self.currentTime, reactant)
            lastItem = reactant
        return result

    def calItoJ(self, i, j):
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
        tt = (1.0 / a0) * math.log((1.0/r1))
        return tt

    def doReaction(self, index):
        reaction = self.reactions[index]
        for reactant in reaction['reactants']:
            self.compound_pool[reactant] -= 1
        for product in reaction['products']:
            self.compound_pool[product] += 1

    def isJOccurs(self, j, a0, r2):
        leftBound = (1.0/a0)*self.calItoJ(0, j-1)
        rightBound = (1.0/a0)*self.calItoJ(0, j)
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
        while self.reaction_time > 0:
            r1 = random.random()
            r2 = random.random()
            if r1 == 0:
                r1 = 0.0000001
            if r2 == 0:
                r2 = 0.0000001
            a0 = self.calA0()
            tt = self.calTT(a0, r1)
            self.reaction_time -= tt
            for i in range(len(self.reactions)):
                if self.isJOccurs(i, a0, r2):
                    self.doReaction(i)
            self.currentTime += tt
            self.history[self.currentTime] = copy.deepcopy(self.compound_pool)

    def getProcess(self):
        sorted_rest = sorted(self.history)
        result = dict()
        for key in sorted_rest:
            result[key] = self.history[key]
        return result


